import os
import re
#import ipywidgets as widgets
import tensorflow as tf
#from IPython import display
from dragnn.protos import spec_pb2
from dragnn.python import graph_builder
from dragnn.python import spec_builder
from dragnn.python import load_dragnn_cc_impl  # This loads the actual op definitions
from dragnn.python import render_parse_tree_graphviz
from dragnn.python import visualization
from google.protobuf import text_format
from syntaxnet import load_parser_ops  # This loads the actual op definitions
from syntaxnet import sentence_pb2
from syntaxnet.ops import gen_parser_ops
from tensorflow.python.platform import tf_logging as logging

SEGMENTER_PATH = os.path.join('/home/lsa/conconexp/models/syntaxnet/examples/dragnn/data/en/segmenter')
PARSER_PATH = os.path.join('/home/lsa/conconexp/models/syntaxnet/examples/dragnn/data/en')


def load_model(base_dir, master_spec_name, checkpoint_name):
    # Read the master spec
    master_spec = spec_pb2.MasterSpec()
    with open(os.path.join(base_dir, master_spec_name), "r") as f:
        text_format.Merge(f.read(), master_spec)
    spec_builder.complete_master_spec(master_spec, None, base_dir)
    logging.set_verbosity(logging.WARN)  # Turn off TensorFlow spam.

    # Initialize a graph
    graph = tf.Graph()
    with graph.as_default():
        hyperparam_config = spec_pb2.GridPoint()
        builder = graph_builder.MasterBuilder(master_spec, hyperparam_config)
        # This is the component that will annotate test sentences.
        annotator = builder.add_annotation(enable_tracing=True)
        builder.add_saver()  # "Savers" can save and load models; here, we're only going to load.

    sess = tf.Session(graph=graph)
    with graph.as_default():
        # sess.run(tf.global_variables_initializer())
        # sess.run('save/restore_all', {'save/Const:0': os.path.join(base_dir, checkpoint_name)})
        builder.saver.restore(sess, os.path.join(base_dir, checkpoint_name))
        
    def annotate_sentence(sentence):
        with graph.as_default():
            return sess.run([annotator['annotations'], annotator['traces']],
                            feed_dict={annotator['input_batch']: [sentence]})
    return annotate_sentence

segmenter_model = load_model(SEGMENTER_PATH, "spec.textproto", "checkpoint")
parser_model = load_model(PARSER_PATH, "parser_spec.textproto", "checkpoint")


def annotate_text(text):
    sentence = sentence_pb2.Sentence(
        text=text,
        token=[sentence_pb2.Token(word=text, start=-1, end=-1)]
    )

    # preprocess
    with tf.Session(graph=tf.Graph()) as tmp_session:
        char_input = gen_parser_ops.char_token_generator([sentence.SerializeToString()])
        preprocessed = tmp_session.run(char_input)[0]
    segmented, _ = segmenter_model(preprocessed)

    annotations, traces = parser_model(segmented[0])
    assert len(annotations) == 1
    assert len(traces) == 1
    tags_list = sentence_pb2.Sentence.FromString(annotations[0])
    return extract_features(tags_list.token)


def extract_features(tags_list):

    counter = 0
    find_line = re.compile(r'fPOS.+?value.+?\}')
    find_tag = re.compile(r'[A-Z]+\++[A-Z]+?\\')

    list_of_tags = []

    while True:

        try:
            tag = str(tags_list[counter])
            s = find_line.findall(tag)[0]
            list_of_tags.append(find_tag.findall(s)[0][:-1])

        except:
            break

        counter += 1

    return list_of_tags


import convolutional_mlp, logistic_cg, logistic_sgd, mlp, SdA, dA, rbm , DBN
from nose.plugins.skip import SkipTest
import numpy, theano
import time, sys


def test_logistic_sgd():
    logistic_sgd.sgd_optimization_mnist(n_epochs=10)


def test_logistic_cg():
    logistic_cg.cg_optimization_mnist(n_epochs=10)


def test_mlp():
    mlp.test_mlp(n_epochs=5)


def test_convolutional_mlp():
    convolutional_mlp.evaluate_lenet5(n_epochs=5,nkerns=[5,5])


def test_dA():
    dA.test_dA(training_epochs = 3, output_folder = 'tmp_dA_plots')


def test_SdA():
    SdA.test_SdA(pretraining_epochs = 2, training_epochs = 3, batch_size = 300)


def test_dbn():
    DBN.test_DBN(pretraining_epochs = 1, training_epochs = 2, batch_size =300)



def test_rbm():
    rbm.test_rbm(training_epochs = 1, batch_size = 300, n_chains = 1, n_samples = 1, 
            output_folder =  'tmp_rbm_plots')


def speed():
    """
    This fonction modify the configuration theano and don't restore it!
    I want it to be compatible with python2.4 so using try: finaly: is not an option.
    """

    import theano
    algo=['logistic_sgd','logistic_cg','mlp','convolutional_mlp','dA','SdA','DBN','rbm']
    to_exec=[True]*len(algo)
#    to_exec[3]=False
#    to_exec=[False]*len(algo)
#    to_exec[3]=True

    expected_times_64=numpy.asarray([  12.42313051   28.09523582  106.35365391  153.62705898  153.12310314
  425.09175086  642.72824597  652.52828193])

    def time_test(m,l,idx,f,**kwargs):
        if not to_exec[idx]:
            l[idx]=float('nan')
            return
        print algo[idx]
        ts=m.call_time
        f(**kwargs)
        te=m.call_time
        l[idx]=te-ts

    def do_tests():
        m=theano.compile.mode.get_default_mode()
        l=numpy.zeros(len(algo))
        time_test(m,l,0, logistic_sgd.sgd_optimization_mnist,n_epochs=30)
        time_test(m,l,1, logistic_cg.cg_optimization_mnist,n_epochs=30)
        time_test(m,l,2, mlp.test_mlp, n_epochs=5)
        time_test(m,l,3, convolutional_mlp.evaluate_lenet5, n_epochs=5,nkerns=[5,5])
        time_test(m,l,4, dA.test_dA, training_epochs = 2, output_folder = 'tmp_dA_plots')
        time_test(m,l,5, SdA.test_SdA, pretraining_epochs = 1, training_epochs = 2, batch_size = 300)
        time_test(m,l,6, DBN.test_DBN, pretraining_epochs = 1, training_epochs = 2, batch_size = 300)
        time_test(m,l,7, rbm.test_rbm, training_epochs = 1, batch_size = 300, n_chains = 1, n_samples = 1, output_folder =  'tmp_rbm_plots')
        return l


    #test in float64 in FAST_RUN mode on the cpu
    print >> sys.stderr, algo
    theano.config.floatX='float64'
    theano.config.mode='FAST_RUN'
    float64_times=do_tests()
    print >> sys.stderr, 'float64 times',float64_times
    print >> sys.stderr, 'float64 expected',expected_times_64
    print >> sys.stderr, '% get/expected',float64_times/expected_times_64
    return

    #test in float32 in FAST_RUN mode on the cpu
    theano.config.floatX='float32'
    float32_times=do_tests()
    print >> sys.stderr, 'float32 times',float32_times

    #test in float64 in FAST_RUN mode on the gpu
    theano.config.device='gpu0'
    import theano.sandbox.cuda
    gpu_times=do_tests()

    print >> sys.stderr, 'float64 times',float64_times
    print >> sys.stderr, 'float32 times',float32_times
    print >> sys.stderr, 'gpu times',gpu_times
    print >> sys.stderr, float64_times/float32_times
    print >> sys.stderr, float64_times/gpu_times
    

from keras.callbacks import EarlyStopping, ModelCheckpoint
from time import strftime
import sys

def train_model(model, X, y, where_to_save, fit_params=None):

    if fit_params is None:
        fit_params = {
            "batch_size": 32,
            "nb_epoch": 15,
            "verbose": True,
            "validation_split": 0.1,
            "callbacks": [EarlyStopping(verbose=True, patience=5, monitor='val_loss'),
                          ModelCheckpoint(where_to_save, monitor='val_loss', verbose=True, save_best_only=True)]
        }
    print 'Fitting! Hit CTRL-C to stop early...'
    history = "Nothing to show"
    try:
        history = model.fit(X, y, **fit_params)
    except KeyboardInterrupt:
        print "Training stopped early!"

    return history

def test_model(model_obj, X_test, y_test, saved_model):
    model_obj.load_weights(saved_model)

    print "getting predictions on the test set"
    yhat = model_obj.predict(X_test, verbose=True, batch_size=50)
    acc = ((yhat.ravel() > 0.5) == (y_test > 0.5)).mean()

    print "Test set accuracy of {}%.".format(acc * 100.0)
    print "Test set error of {}%. Exiting...".format((1 - acc) * 100.0)

    return acc

def write_log(model, history, code_file, acc, log_file):
    # TODO: A bit tacky...watch out the sys.stdout thing...the terminal might disappear!!
    sys.stdout = open(log_file, 'w')

    print ("Model trained at " + strftime("%Y-%m-%d %H:%M:%S"))
    print ("Accuracy obtained: " + str(acc))
    print ("Error obtained: " + str(1 - acc))
    print ("==" * 40)
    print ("Model in json:")
    print ("==" * 40)
    print model.to_json()
    print ("==" * 40)
    print "Model summary:"
    print ("==" * 40)
    model.summary()
    print ("==" * 40)
    print ("Training history:")
    print ("==" * 40)
    print (history)
    print ("==" * 40)
    print ("Code file:")
    print ("==" * 40)
    with open(code_file) as code:
        print (code.read())

    sys.stdout = sys.__stdout__
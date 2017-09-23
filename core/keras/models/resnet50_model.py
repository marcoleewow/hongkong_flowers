from keras.layers import *
from keras.models import Model, Sequential
from keras.applications import ResNet50

# note that for keras these are functions!
def resnet50_model(args, num_classes):

    # build the ResNet50 network
    model = ResNet50(weights='imagenet', include_top=False, input_shape=args.img_size)
    print('Model loaded.')

    # set the first 80 layers (up to the last conv block)
    # to non-trainable (weights will not be updated)
    for layer in model.layers:
        layer.trainable = True

    for layer in model.layers[:80]:
        layer.trainable = False

    # build a classifier model to put on top of the convolutional model
    y = model.output
    y = Flatten()(y)
    y = Dropout(args.dropout)(y)

    # now the shape = (batch_size, 2048)
    y = Dense(2048, activation='elu', name='new_fc1')(y)
    y = Dropout(args.dropout)(y)
    y = Dense(1024, activation='elu', name='new_fc2')(y)
    y = Dropout(args.dropout)(y)
    y = Dense(512, activation='elu', name='new_fc3')(y)
    y = Dropout(args.dropout)(y)

    predictions = Dense(num_classes, activation='softmax', name='new_predictions2')(y)

    model = Model(model.input, predictions, name='resnet50')

    return model

import numpy as np

from neupy.utils import format_data, iters
from neupy.core.properties import BoundedProperty, IntProperty
from neupy.algorithms.base import BaseSkeleton
from neupy.exceptions import NotTrained
from neupy.algorithms.rbfn.utils import pdf_between_data


__all__ = ('PNN',)


class PNN(BaseSkeleton):


    std = BoundedProperty(minval=0)
    batch_size = IntProperty(default=128, minval=0, allow_none=True)

    def __init__(self, std, batch_size=128, verbose=False):
        self.std = std
        self.batch_size = batch_size

        self.classes = None
        self.X_train = None
        self.y_train = None

        super(PNN, self).__init__(batch_size=batch_size, verbose=verbose)

    def train(self, X_train, y_train, copy=True):

        X_train = format_data(X_train, copy=copy)
        y_train = format_data(y_train, copy=copy, make_float=False)

        self.X_train = X_train
        self.y_train = y_train

        if X_train.shape[0] != y_train.shape[0]:
            raise ValueError(
                "Number of samples in the input and "
                "target datasets are different")

        if y_train.shape[1] != 1:
            raise ValueError(
                "Target value should be vector or "
                "matrix with only one column")

        classes = self.classes = np.unique(y_train)
        n_classes = classes.size
        n_samples = X_train.shape[0]

        class_ratios = self.class_ratios = np.zeros(n_classes)
        row_comb_matrix = self.row_comb_matrix = np.zeros(
            (n_classes, n_samples))

        for i, class_name in enumerate(classes):
            class_name = classes[i]
            class_val_positions = (y_train == class_name)
            row_comb_matrix[i, class_val_positions.ravel()] = 1
            class_ratios[i] = np.sum(class_val_positions)

    def predict_proba(self, X):

        outputs = iters.apply_batches(
            function=self.predict_raw,
            inputs=format_data(X),
            batch_size=self.batch_size,
            show_progressbar=self.logs.enable,
        )
        raw_output = np.concatenate(outputs, axis=1)

        total_output_sum = raw_output.sum(axis=0).reshape((-1, 1))
        return raw_output.T / total_output_sum

    def predict_proba_output(self, X):

        outputs = iters.apply_batches(
            function=self.predict_raw,
            inputs=format_data(X),
            batch_size=self.batch_size,
            show_progressbar=self.logs.enable,
        )
        raw_output = np.concatenate(outputs, axis=1)

        return raw_output.T

    def predict_raw(self, X):

        if self.classes is None:
            raise NotTrained(
                "Cannot make a prediction. Network hasn't been trained yet")

        if X.shape[1] != self.X_train.shape[1]:
            raise ValueError(
                "Input data must contain {0} features, got {1}"
                "".format(self.X_train.shape[1],  X.shape[1]))

        class_ratios = self.class_ratios.reshape((-1, 1))
        pdf_outputs = pdf_between_data(self.X_train, X, self.std)

        return np.dot(self.row_comb_matrix, pdf_outputs) / class_ratios

    def predict(self, X):

        outputs = iters.apply_batches(
            function=self.predict_raw,
            inputs=format_data(X),
            batch_size=self.batch_size,
            show_progressbar=self.logs.enable,
        )

        raw_output = np.concatenate(outputs, axis=1)
        return self.classes[raw_output.argmax(axis=0)]

import unittest
import tempfile
import numpy as np
import pandas as pd
from preprocessing_utils import PreprocessingUtils
from preprocessing_categorical import PreprocessingCategorical


class PreprocessingCategoricalIntegersTest(unittest.TestCase):

    def test_constructor_preprocessing_categorical(self):
        '''
            Check if PreprocessingCategorical object is properly initialized
        '''
        categorical = PreprocessingCategorical(PreprocessingCategorical.CONVERT_INTEGER)
        self.assertEqual(categorical._convert_method, PreprocessingCategorical.CONVERT_INTEGER)
        self.assertEqual(categorical._convert_params, {})


    def test_fit_integers(self):
        # training data
        d = {
                'col1': [1, 2, 3],
                'col2': ['a', 'a', 'c'],
                'col3': [1, 1, 3],
                'col4': ['a', 'b', 'c']
            }
        df = pd.DataFrame(data=d)
        categorical = PreprocessingCategorical(PreprocessingCategorical.CONVERT_INTEGER)
        categorical.fit(df)

        self.assertTrue('col2' in categorical._convert_params)
        self.assertTrue('col4' in categorical._convert_params)
        self.assertTrue('a' in categorical._convert_params['col2'])
        self.assertTrue('c' in categorical._convert_params['col2'])
        self.assertTrue('b' not in categorical._convert_params['col2'])
        self.assertTrue('a' in categorical._convert_params['col4'])
        self.assertTrue('b' in categorical._convert_params['col4'])
        self.assertTrue('c' in categorical._convert_params['col4'])


    def test_fit_transform_integers(self):
        # training data
        d = {
                'col1': [1, 2, 3],
                'col2': ['a', 'a', 'c'],
                'col3': [1, 1, 3],
                'col4': ['a', 'b', 'c']
            }
        df = pd.DataFrame(data=d)
        categorical = PreprocessingCategorical(PreprocessingCategorical.CONVERT_INTEGER)
        categorical.fit(df)
        df = categorical.transform(df)
        for col in ['col1', 'col2', 'col3', 'col4']:
            self.assertTrue(col in df.columns)
        self.assertEqual(df['col2'][0], 0)
        self.assertEqual(df['col2'][1], 0)
        self.assertEqual(df['col2'][2], 1)
        self.assertEqual(df['col4'][0], 0)
        self.assertEqual(df['col4'][1], 1)
        self.assertEqual(df['col4'][2], 2)



    def test_fit_transform_integers_with_new_values(self):
        # training data
        d_train = {
                'col1': [1, 2, 3],
                'col2': ['a', 'a', 'c'],
                'col3': [1, 1, 3],
                'col4': ['a', 'b', 'c']
            }
        df_train = pd.DataFrame(data=d_train)
        categorical = PreprocessingCategorical(PreprocessingCategorical.CONVERT_INTEGER)
        categorical.fit(df_train)
        # testing data
        d = {
                'col1': [1, 2, 3],
                'col2': ['a', 'd', 'f'],
                'col3': [1, 1, 3],
                'col4': ['e', 'b', 'z']
            }
        df = pd.DataFrame(data=d)
        df = categorical.transform(df)
        for col in ['col1', 'col2', 'col3', 'col4']:
            self.assertTrue(col in df.columns)
        self.assertEqual(df['col2'][0], 0)
        self.assertEqual(df['col2'][1], 2) # new values get higher indexes
        self.assertEqual(df['col2'][2], 3) # new values get higher indexes
        self.assertEqual(df['col4'][0], 3) # new values get higher indexes
        self.assertEqual(df['col4'][1], 1)
        self.assertEqual(df['col4'][2], 4) # new values get higher indexes


    def test_to_and_from_json_convert_integers(self):
        # training data
        d = {
                'col1': [1, 2, 3],
                'col2': ['a', 'a', 'c'],
                'col3': [1, 1, 3],
                'col4': ['a', 'b', 'c']
            }
        df = pd.DataFrame(data=d)
        cat1 = PreprocessingCategorical(PreprocessingCategorical.CONVERT_INTEGER)
        cat1.fit(df)

        cat2 = PreprocessingCategorical(PreprocessingCategorical.CONVERT_INTEGER)
        cat2.from_json(cat1.to_json())
        df = cat2.transform(df)
        for col in ['col1', 'col2', 'col3', 'col4']:
            self.assertTrue(col in df.columns)
        self.assertEqual(df['col2'][0], 0)
        self.assertEqual(df['col2'][1], 0)
        self.assertEqual(df['col2'][2], 1)
        self.assertEqual(df['col4'][0], 0)
        self.assertEqual(df['col4'][1], 1)
        self.assertEqual(df['col4'][2], 2)

    def test_save_and_load_convert_integers(self):
        # training data
        d = {
                'col1': [1, 2, 3],
                'col2': ['a', 'a', 'c'],
                'col3': [1, 1, 3],
                'col4': ['a', 'b', 'c']
            }
        df = pd.DataFrame(data=d)
        cat1 = PreprocessingCategorical(PreprocessingCategorical.CONVERT_INTEGER)
        cat1.fit(df)

        cat2 = PreprocessingCategorical(PreprocessingCategorical.CONVERT_INTEGER)
        with tempfile.NamedTemporaryFile() as temp:
            cat1.save(temp.name)
            cat2.load(temp.name)
        df = cat2.transform(df)
        for col in ['col1', 'col2', 'col3', 'col4']:
            self.assertTrue(col in df.columns)
        self.assertEqual(df['col2'][0], 0)
        self.assertEqual(df['col2'][1], 0)
        self.assertEqual(df['col2'][2], 1)
        self.assertEqual(df['col4'][0], 0)
        self.assertEqual(df['col4'][1], 1)
        self.assertEqual(df['col4'][2], 2)


if __name__ == '__main__':
    unittest.main()

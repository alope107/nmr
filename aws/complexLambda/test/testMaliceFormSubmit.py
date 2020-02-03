from unittest import TestCase
from re import compile, IGNORECASE
import io
from complexLambda.maliceFormSubmit import validate_csv
from complexLambda import maliceFormSubmit

class TestValidateCSV(TestCase):

    def test_valid(self):
        valid_str = "residue,15N,1H,intensity,titrant,visible\n" + \
                    "6,124.567,7.763,3248421,0,150\n" + \
                    "63,1243.567,72.763,3248421,8.3,150"
        valid_io = io.StringIO(valid_str)
        self.assertIsNone(validate_csv(valid_io))

    def test_bad_header(self):
        invalid_str = "residue,15N,1H,intensity,tit,obs\n" + \
                      "6,124.567,7.763,3248421,0,150\n" + \
                      "63,1243.567,72.763,3248421,8.3,150"
        invalid_io = io.StringIO(invalid_str)
        with self.assertRaisesRegex(ValueError, compile("header", IGNORECASE)):
            validate_csv(invalid_io)

    def test_empty(self):
        empty_io = io.StringIO("")
        with self.assertRaisesRegex(ValueError, compile("empty", IGNORECASE)):
            validate_csv(empty_io)

    def test_nonnumeric(self):
        invalid_str = "residue,15N,1H,intensity,titrant,visible\n" + \
                      "6,124.567,7.763,3248421,0,150\n" + \
                      "63,1243.567,NOTANUMBER,3248421,8.3,150"
        invalid_io = io.StringIO(invalid_str)
        with self.assertRaisesRegex(ValueError, compile("convert", IGNORECASE)):
            validate_csv(invalid_io)

    def test_missing(self):
        invalid_str = "residue,15N,1H,intensity,titrant,visible\n" + \
                      "6,,7.763,3248421,0,150\n" + \
                      "63,1243.567,72.763,3248421,8.3,150"
        invalid_io = io.StringIO(invalid_str)
        with self.assertRaisesRegex(ValueError, compile("missing", IGNORECASE)):
            validate_csv(invalid_io)
    
    def test_too_few_col(self):
        invalid_str = "residue,15N,1H,intensity,titrant,visible\n" + \
                      "6,7.763,3248421,0,150\n" + \
                      "63,1243.567,72.763,3248421,8.3,150"
        invalid_io = io.StringIO(invalid_str)
        with self.assertRaisesRegex(ValueError, compile("values", IGNORECASE)):
            validate_csv(invalid_io)

    def test_too_many_col(self):
        invalid_str = "residue,15N,1H,intensity,titrant,visible\n" + \
                      "6,5,5,5,7.763,3248421,0,150\n" + \
                      "63,1243.567,72.763,3248421,8.3,150"
        invalid_io = io.StringIO(invalid_str)
        with self.assertRaisesRegex(ValueError, compile("values", IGNORECASE)):
            validate_csv(invalid_io)

def integration_test():
    maliceFormSubmit.KEY_PREFIX = "test/" + maliceFormSubmit.KEY_PREFIX
    maliceFormSubmit.fetch_and_upload("11KI1D-j15y81ZBGYq6KTkVW29Luy5waQ", "auberonlopez@gmail.com")
        
if __name__=="__main__":
    print("Running integration test")
    integration_test()

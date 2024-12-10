from tests.test_h1_existence import test_h1_existence
from tests.test_html_sequence import test_html_sequence
from tests.test_img import test_img
from tests.test_url import test_url
from tests.test_currency_filter import test_currency_filter
from tests.test_scripts import test_scripts

if __name__ == "__main__":
    test_h1_existence()
    test_html_sequence()
    test_img()
    test_url()
    test_currency_filter()
    test_scripts()


    print("Tests completed. Check the 'reports/test_results.xlsx' for results.")

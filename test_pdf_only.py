#!/usr/bin/env python3

from backend_test import AMSafeAPITester

if __name__ == "__main__":
    tester = AMSafeAPITester()
    tester.run_pdf_tests_only()
Vint
====

[![Build Status](https://travis-ci.org/Kuniwak/viml-lint.svg?branch=master)](https://travis-ci.org/Kuniwak/vint)

Vint is a faster and highly extensible Vim script Language Lint.
This is implemented by Python 3.4.x.

**But now, Vint is under development.**


How to Add New Policy
---------------------

1. Write both valid/invalid Vim scripts to check

	Write both valid/invalid Vim scripts and put its to the fixture directory as `test/fixture/policy/policyname_valid.vim`.


2. Write a test code

	You can test easily by using `test.asserting.policy.PolicyAssertion`.

		import unittest
		from test.asserting.policy import PolicyAssertion
		from test.asserting.policy import get_fixture_path

		from lib.linting.level import Levels
		from lib.linting.policy.my_policy import MyPolicy

		PATH_VALID_VIM_SCRIPT = get_fixture_path('my_policy_valid.vim')
		PATH_INVALID_VIM_SCRIPT = get_fixture_path('my_policy_invalid.vim')


		class TestMyPolicy(PolicyAssertion, unittest.TestCase):
			def test_get_violation_if_found(self):
				# Expect no violations found
				self.assertFoundViolationsEqual(PATH_VALID_VIM_SCRIPT, MyPolicy, [])

				expected_violations = [
					{
						'name': 'MyPolicy',
						'level': Levels['WARNING'],
						'position': {
							'line': 2,
							'column': 6,
							'path': PATH_INVALID_VIM_SCRIPT
						},
					},
					{
						'name': 'MyPolicy',
						'level': Levels['WARNING'],
						'position': {
							'line': 3,
							'column': 6,
							'path': PATH_INVALID_VIM_SCRIPT
						},
					},
				]

				self.assertFoundViolationsEqual(PATH_VALID_VIM_SCRIPT, MyPolicy, expected_violations)

		if __name__ == '__main__':
			unittest.main()

3. Write a policy code

	You should inherit `lib.linting.policy.AbstractPolicy` and implement 2 methods;

	 * `is_valid(Node: ast_node, Environment: env): Boolean`

		This method should return whether the given node is valid for the policy as Boolean.
		And you can use an environment that has `root_ast: Node` and `file path: String` to
		special lint.

	 * `listen_node_type(): NodeType[]`

		This method should return listened `NodeType` such as `NodeType['STRING']`.

4. Run the test

		$ py.test test

	or

		$ python -m unittest discover test


License
-------

[MIT](http://orgachem.mit-license.org/)


Acknowledgement
---------------

* [ynkdir/vim-vimlparser](https://github.com/ynkdir/vim-vimlparser)
* [Google Vimscript Style Guide](http://google-styleguide.googlecode.com/svn/trunk/vimscriptguide.xml?showone=Catching_Exceptions#Catching_Exceptions)
/**
 * :copyright (c) 2014 - 2017, The Regents of the University of California, through Lawrence Berkeley National Laboratory (subject to receipt of any required approvals from the U.S. Department of Energy) and contributors. All rights reserved.
 * :author
 */
// create dummy angularJS app to attach filter(s)
var myTypedNumberFilterApp = angular.module('myTypedNumberFilterApp', ['typedNumber']);

describe('The typedNumber filter', function () {
  beforeEach(module('myTypedNumberFilterApp'));
  it('should parse strings as strings and return them',
    inject(function (typedNumberFilter) {
      expect(typedNumberFilter('tester')).toBe('tester');
    })
  );
  it('should parse strings as strings and return them, even if they look like numbers',
    inject(function (typedNumberFilter) {
      expect(typedNumberFilter('123.1456')).toBe('123.1456');
    })
  );

  it('should parse numbers as numbers and return them',
    inject(function (typedNumberFilter) {
      expect(typedNumberFilter('123.00001', 'number')).toBe('123');
    })
  );

  it('should allow the user to set the number of sig digits',
    inject(function (typedNumberFilter) {
      expect(typedNumberFilter('123.321', 'number', 'not_year', 1)).toBe('123.3');
    })
  );

  it('should add commas to number greater than 999',
    inject(function (typedNumberFilter) {
      expect(typedNumberFilter('123456789', 'number', 'not_year', 0)).toBe('123,456,789');
    })
  );

  it('should parse year_built and not add commas',
    inject(function (typedNumberFilter) {
      expect(typedNumberFilter('1946', 'number', 'year_built', 1)).toBe('1946');
    })
  );
});

/**
 * :copyright (c) 2014 - 2017, The Regents of the University of California, through Lawrence Berkeley National Laboratory (subject to receipt of any required approvals from the U.S. Department of Energy) and contributors. All rights reserved.
 * :author
 */
angular.module('BE.seed.controller.create_note_modal', [])
.controller('create_note_modal_controller', [
  '$scope',
  '$uibModalInstance',
  'audit_service',
  '$timeout',
  'building',
  'note',
  function ($scope, $uibModalInstance, audit_service, $timeout, building, note) {
    $scope.note = note || {};
    $scope.note = angular.copy($scope.note);
    $scope.error_message = '';

    /**
     * saves a new note or updates an existing note
     */
    $scope.submit_form = function () {
      if (!_.isUndefined(note)) {
        // update existing note
        audit_service.update_note(note.id, $scope.note.action_note)
          .then(function (data) {
            $uibModalInstance.close(data.audit_log);
          }, function (data) {
            $scope.error_message = data.message;
          });
      } else {
        // new note
        audit_service.create_note(building.canonical_building, $scope.note.action_note)
          .then(function (data) {
            $uibModalInstance.close(data.audit_log);
          }, function (data) {
            $scope.error_message = data.message;
          });
      }
    };

    $scope.close = function () {
      $uibModalInstance.close($scope.note);
    };

    $scope.cancel = function () {
      $uibModalInstance.dismiss('cancel');
    };

    /**
     * set the focus on the first input box
     */
    $timeout(function () {
      angular.element('#creatNote').focus();
    }, 50);
  }]);

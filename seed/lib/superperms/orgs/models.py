# !/usr/bin/env python
# encoding: utf-8
"""
:copyright (c) 2014 - 2015, The Regents of the University of California, through Lawrence Berkeley National Laboratory (subject to receipt of any required approvals from the U.S. Department of Energy) and contributors. All rights reserved.  # NOQA
:author
"""
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

from seed.lib.superperms.orgs.exceptions import TooManyNestedOrgs

USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', User)


# Role Levels
ROLE_VIEWER = 0
ROLE_MEMBER = 10
ROLE_OWNER = 20

ROLE_LEVEL_CHOICES = (
    (ROLE_VIEWER, 'Viewer'),
    (ROLE_MEMBER, 'Member'),
    (ROLE_OWNER, 'Owner'),
)


# Invite status
STATUS_PENDING = 'pending'
STATUS_ACCEPTED = 'accepted'
STATUS_REJECTED = 'rejected'

STATUS_CHOICES = (
    (STATUS_PENDING, 'Pending'),
    (STATUS_ACCEPTED, 'Accepted'),
    (STATUS_REJECTED, 'Rejected'),
)


class ExportableField(models.Model):
    """Tracks which model fields are exportable."""

    class Meta:
        unique_together = ('field_model', 'name', 'organization')
        ordering = ['organization', 'name']

    # For relating to the model-type whose fields we're exporting.
    field_model = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    organization = models.ForeignKey(
        'Organization', related_name='exportable_fields'
    )

    def __unicode__(self):
        return u'ExportableField: {0} <{1}> {2}'.format(
            self.field_model, self.name, self.organization.name
        )


class OrganizationUser(models.Model):
    class Meta:
        ordering = ['organization', '-role_level']

    user = models.ForeignKey(USER_MODEL)
    organization = models.ForeignKey('Organization')
    status = models.CharField(
        max_length=12, default=STATUS_PENDING, choices=STATUS_CHOICES
    )
    role_level = models.IntegerField(
        default=ROLE_OWNER, choices=ROLE_LEVEL_CHOICES
    )

    def delete(self, *args, **kwargs):
        """Ensure we preserve at least one Owner for this org."""
        # If we're removing an owner
        if self.role_level == ROLE_OWNER:
            # If there are users, but no other owners in this organization.
            if (
                        OrganizationUser.objects.all().exclude(pk=self.pk).exists() and
                            OrganizationUser.objects.filter(
                                organization=self.organization,
                                role_level=ROLE_OWNER
                            ).exclude(pk=self.pk).count() == 0
            ):
                # Make next most high ranking person the owner.
                other_user = OrganizationUser.objects.filter(
                    organization=self.organization
                ).exclude(pk=self.pk)[0]

                other_user.role_level = ROLE_OWNER
                other_user.save()

        super(OrganizationUser, self).delete(*args, **kwargs)

    def __unicode__(self):
        return u'OrganizationUser: {0} <{1}> ({2})'.format(
            self.user.username, self.organization.name, self.pk
        )


class Organization(models.Model):
    """A group of people that optionally contains another sub group."""

    class Meta:
        ordering = ['name']

    name = models.CharField(max_length=100)
    users = models.ManyToManyField(
        USER_MODEL,
        through=OrganizationUser,
        related_name='orgs',
    )

    parent_org = models.ForeignKey(
        'Organization', blank=True, null=True, related_name='child_orgs'
    )

    # If below this threshold, we don't show results from this Org
    # in exported views of its data.
    query_threshold = models.IntegerField(max_length=4, blank=True, null=True)

    def save(self, *args, **kwargs):
        """Perform checks before saving."""
        # There can only be one.
        if (
                        self.parent_org is not None and
                        self.parent_org.parent_org is not None
        ):
            raise TooManyNestedOrgs

        super(Organization, self).save(*args, **kwargs)

    def is_member(self, user):
        """Return True if user object has a relation to this organization."""
        return user in self.users.all()

    def add_member(self, user, role=ROLE_OWNER):
        """Add a user to an organization."""
        return OrganizationUser.objects.get_or_create(
            user=user, organization=self, role_level=role
        )

    def remove_member(self, user):
        """Remove user from organization."""
        return OrganizationUser.objects.get(
            user=user, organization=self
        ).delete()

    def is_owner(self, user):
        """
        Return True if the user has a relation to this org, with a role of
        owner.
        """
        return OrganizationUser.objects.filter(
            user=user, role_level=ROLE_OWNER, organization=self,
        ).exists()

    def get_exportable_fields(self):
        """Default to parent definition of exportable fields."""
        if self.parent_org:
            return self.parent_org.get_exportable_fields()
        return self.exportable_fields.all()

    def get_query_threshold(self):
        """Default to parent definition of query threshold."""
        if self.parent_org:
            return self.parent_org.get_query_threshold()
        return self.query_threshold

    @property
    def is_parent(self):
        return not self.parent_org

    def get_parent(self):
        """
        Returns the top-most org in this org's tree.
        That could be this org, or it could be this org's parent.
        """
        if self.is_parent:
            return self
        return self.parent_org

    def __unicode__(self):
        return u'Organization: {0}({1})'.format(self.name, self.pk)

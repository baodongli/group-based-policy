#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from neutron.api import extensions
from neutron.api.v2 import attributes as attr

from gbpservice.neutron.extensions import group_policy as gp


CISCO_APIC_GBP_SEGMENTATION_LABEL_EXT = 'cisco_apic_gbp_label_segmentation'


def _validate_list_of_unique_strings(data, max_string_len=None):
    if not isinstance(data, list):
        msg = _("'%s' is not a list") % data
        return msg
    if len(set(data)) != len(data):
        msg = _("Duplicate items in the list: '%s'") % ', '.join(data)
        return msg
    for item in data:
        msg = attr._validate_string(item, max_string_len)
        if msg:
            return msg


attr.validators['type:list_of_unique_strings'] = (
    _validate_list_of_unique_strings)


EXTENDED_ATTRIBUTES_2_0 = {
    gp.POLICY_TARGETS: {
        'segmentation_labels': {
            'allow_post': True, 'allow_put': True, 'default': None,
            'validate': {'type:list_of_unique_strings': None},
            'convert_to': attr.convert_none_to_empty_list,
            'is_visible': True},
    },
}


class Apic_segmentation_label(extensions.ExtensionDescriptor):

    @classmethod
    def get_name(cls):
        return "APIC GBP Segmentation Extension"

    @classmethod
    def get_alias(cls):
        return CISCO_APIC_GBP_SEGMENTATION_LABEL_EXT

    @classmethod
    def get_description(cls):
        return _("This extension supports a list of (micro)segmentation "
                 "labels that can be applied to the Policy Target resource.")

    @classmethod
    def get_updated(cls):
        return "2016-08-03T10:00:00-00:00"

    def get_extended_resources(self, version):
        if version == "2.0":
            return EXTENDED_ATTRIBUTES_2_0
        else:
            return {}
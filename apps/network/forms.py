from django import forms
from django.utils.translation import gettext_lazy as _

from apps.network.models import Device, DeviceGroup, NetworkSettings


class DeviceForm(forms.ModelForm):
    """Form for creating and updating devices."""

    class Meta:
        model = Device
        fields = [
            'name', 'device_type', 'manufacturer', 'mac_address', 'ip_address',
            'signal_strength', 'upload_speed', 'download_speed', 'status',
            'owner', 'group', 'notes'
        ]
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
            'connected_since': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['owner'].required = False
        self.fields['group'].required = False
        self.fields['manufacturer'].required = False


class DeviceGroupForm(forms.ModelForm):
    """Form for creating and updating device groups."""

    class Meta:
        model = DeviceGroup
        fields = ['name', 'description', 'color']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'color': forms.TextInput(attrs={'type': 'color'}),
        }


class NetworkSettingsForm(forms.ModelForm):
    """Form for network settings."""

    class Meta:
        model = NetworkSettings
        fields = [
            'ssid', 'password', 'guest_network_enabled', 'guest_ssid',
            'guest_password', 'security_mode', 'wifi_channel',
            'bandwidth_limit_mbps', 'dhcp_enabled', 'dhcp_start_ip',
            'dhcp_end_ip', 'dns_primary', 'dns_secondary', 'lan_ip'
        ]
        widgets = {
            'password': forms.PasswordInput(render_value=True),
            'guest_password': forms.PasswordInput(render_value=True),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['guest_password'].required = False
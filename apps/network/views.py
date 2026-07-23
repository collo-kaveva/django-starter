from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count, Q, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.network.decorators import administrator_required, technician_or_administrator_required
from apps.network.forms import DeviceForm, DeviceGroupForm, NetworkSettingsForm
from apps.network.models import Alert, Device, DeviceGroup, NetworkSettings, TrafficLog


@technician_or_administrator_required
def dashboard(request):
    """Main dashboard with network statistics and charts."""

    # Get network statistics
    total_devices = Device.objects.count()
    online_devices = Device.objects.filter(status=Device.Status.ONLINE).count()
    offline_devices = Device.objects.filter(status=Device.Status.OFFLINE).count()
    blocked_devices = Device.objects.filter(status=Device.Status.BLOCKED).count()

    # Calculate simulated network stats
    avg_upload = Device.objects.filter(status=Device.Status.ONLINE).aggregate(avg=Sum("upload_speed"))["avg"] or 0
    avg_download = Device.objects.filter(status=Device.Status.ONLINE).aggregate(avg=Sum("download_speed"))["avg"] or 0

    # Get recent alerts
    recent_alerts = Alert.objects.filter(is_read=False).order_by("-created_at")[:5]

    # Get top bandwidth consumers
    top_consumers = Device.objects.filter(status=Device.Status.ONLINE).order_by("-download_speed")[:5]

    # Get device groups with counts
    device_groups = DeviceGroup.objects.annotate(device_count=Count("devices")).order_by("-device_count")

    # Get recent traffic data for charts (last 24 hours)
    twenty_four_hours_ago = timezone.now() - timezone.timedelta(hours=24)
    recent_traffic = TrafficLog.objects.filter(timestamp__gte=twenty_four_hours_ago).order_by("timestamp")

    context = {
        "active_tab": "dashboard",
        "page_title": _("Dashboard"),
        "total_devices": total_devices,
        "online_devices": online_devices,
        "offline_devices": offline_devices,
        "blocked_devices": blocked_devices,
        "avg_upload": avg_upload,
        "avg_download": avg_download,
        "recent_alerts": recent_alerts,
        "top_consumers": top_consumers,
        "device_groups": device_groups,
        "recent_traffic": recent_traffic,
    }

    return render(request, "network/dashboard.html", context)


@technician_or_administrator_required
def device_list(request):
    """List all devices with search, filter, and sorting."""

    search_query = request.GET.get("search", "")
    status_filter = request.GET.get("status", "")
    group_filter = request.GET.get("group", "")
    type_filter = request.GET.get("type", "")
    sort_by = request.GET.get("sort", "-last_seen")

    devices = Device.objects.all()

    # Apply search
    if search_query:
        devices = devices.filter(
            Q(name__icontains=search_query)
            | Q(mac_address__icontains=search_query)
            | Q(ip_address__icontains=search_query)
            | Q(manufacturer__icontains=search_query)
        )

    # Apply filters
    if status_filter:
        devices = devices.filter(status=status_filter)
    if group_filter:
        devices = devices.filter(group_id=group_filter)
    if type_filter:
        devices = devices.filter(device_type=type_filter)

    # Apply sorting
    valid_sort_fields = [
        "name",
        "-name",
        "last_seen",
        "-last_seen",
        "download_speed",
        "-download_speed",
        "upload_speed",
        "-upload_speed",
    ]
    if sort_by in valid_sort_fields:
        devices = devices.order_by(sort_by)

    # Pagination
    paginator = Paginator(devices, 20)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    # Get filter options
    device_groups = DeviceGroup.objects.all()

    context = {
        "active_tab": "devices",
        "page_title": _("Devices"),
        "page_obj": page_obj,
        "devices": page_obj,
        "search_query": search_query,
        "status_filter": status_filter,
        "group_filter": group_filter,
        "type_filter": type_filter,
        "sort_by": sort_by,
        "device_groups": device_groups,
        "device_types": Device.DeviceType.choices,
        "status_choices": Device.Status.choices,
    }

    return render(request, "network/device_list.html", context)


@technician_or_administrator_required
def device_detail(request, device_id):
    """View device details."""
    device = get_object_or_404(Device, id=device_id)
    traffic_logs = device.traffic_logs.order_by("-timestamp")[:50]

    context = {
        "active_tab": "devices",
        "page_title": f"{device.name}",
        "device": device,
        "traffic_logs": traffic_logs,
    }

    return render(request, "network/device_detail.html", context)


@administrator_required
def device_create(request):
    """Create a new device."""
    if request.method == "POST":
        form = DeviceForm(request.POST)
        if form.is_valid():
            device = form.save(commit=False)
            device.save()
            messages.success(request, _("Device created successfully."))
            return redirect("network:device_detail", device_id=device.id)
    else:
        form = DeviceForm()

    context = {
        "active_tab": "devices",
        "page_title": _("Create Device"),
        "form": form,
    }

    return render(request, "network/device_form.html", context)


@administrator_required
def device_update(request, device_id):
    """Update an existing device."""
    device = get_object_or_404(Device, id=device_id)

    if request.method == "POST":
        form = DeviceForm(request.POST, instance=device)
        if form.is_valid():
            form.save()
            messages.success(request, _("Device updated successfully."))
            return redirect("network:device_detail", device_id=device.id)
    else:
        form = DeviceForm(instance=device)

    context = {
        "active_tab": "devices",
        "page_title": _("Update Device"),
        "form": form,
        "device": device,
    }

    return render(request, "network/device_form.html", context)


@administrator_required
def device_delete(request, device_id):
    """Delete a device."""
    device = get_object_or_404(Device, id=device_id)

    if request.method == "POST":
        device.delete()
        messages.success(request, _("Device deleted successfully."))
        return redirect("network:device_list")

    context = {
        "active_tab": "devices",
        "page_title": _("Delete Device"),
        "device": device,
    }

    return render(request, "network/device_confirm_delete.html", context)


@administrator_required
def device_disconnect(request, device_id):
    """Simulate disconnecting a device."""
    device = get_object_or_404(Device, id=device_id)

    if request.method == "POST":
        device.status = Device.Status.OFFLINE
        device.save()
        messages.success(request, _(f"{device.name} has been disconnected."))
        return redirect("network:device_detail", device_id=device.id)

    context = {
        "active_tab": "devices",
        "page_title": _("Disconnect Device"),
        "device": device,
    }

    return render(request, "network/device_confirm_disconnect.html", context)


@administrator_required
def device_block(request, device_id):
    """Simulate blocking a device."""
    device = get_object_or_404(Device, id=device_id)

    if request.method == "POST":
        device.status = Device.Status.BLOCKED
        device.save()
        messages.success(request, _(f"{device.name} has been blocked."))
        return redirect("network:device_detail", device_id=device.id)

    context = {
        "active_tab": "devices",
        "page_title": _("Block Device"),
        "device": device,
    }

    return render(request, "network/device_confirm_block.html", context)


@administrator_required
def device_unblock(request, device_id):
    """Unblock a device."""
    device = get_object_or_404(Device, id=device_id)

    if request.method == "POST":
        device.status = Device.Status.ONLINE
        device.save()
        messages.success(request, _(f"{device.name} has been unblocked."))
        return redirect("network:device_detail", device_id=device.id)

    context = {
        "active_tab": "devices",
        "page_title": _("Unblock Device"),
        "device": device,
    }

    return render(request, "network/device_confirm_unblock.html", context)


@technician_or_administrator_required
def alert_list(request):
    """List all alerts."""
    alerts = Alert.objects.all().order_by("-created_at")

    # Filter by read status
    show_read = request.GET.get("show_read", "all")
    if show_read == "unread":
        alerts = alerts.filter(is_read=False)
    elif show_read == "read":
        alerts = alerts.filter(is_read=True)

    # Filter by severity
    severity_filter = request.GET.get("severity", "")
    if severity_filter:
        alerts = alerts.filter(severity=severity_filter)

    # Pagination
    paginator = Paginator(alerts, 20)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    context = {
        "active_tab": "alerts",
        "page_title": _("Alerts"),
        "page_obj": page_obj,
        "alerts": page_obj,
        "show_read": show_read,
        "severity_filter": severity_filter,
        "severity_choices": Alert.Severity.choices,
    }

    return render(request, "network/alert_list.html", context)


@technician_or_administrator_required
def alert_mark_read(request, alert_id):
    """Mark an alert as read."""
    alert = get_object_or_404(Alert, id=alert_id)

    if request.method == "POST":
        alert.is_read = True
        alert.save()
        messages.success(request, _("Alert marked as read."))
        return redirect("network:alert_list")

    return redirect("network:alert_list")


@technician_or_administrator_required
def alert_mark_all_read(request):
    """Mark all alerts as read."""
    if request.method == "POST":
        Alert.objects.filter(is_read=False).update(is_read=True)
        messages.success(request, _("All alerts marked as read."))
        return redirect("network:alert_list")

    return redirect("network:alert_list")


@administrator_required
def network_settings(request):
    """View and edit network settings."""
    settings_obj = NetworkSettings.objects.first()

    if not settings_obj:
        settings_obj = NetworkSettings.objects.create()

    if request.method == "POST":
        form = NetworkSettingsForm(request.POST, instance=settings_obj)
        if form.is_valid():
            form.save()
            messages.success(request, _("Network settings updated successfully."))
            return redirect("network:network_settings")
    else:
        form = NetworkSettingsForm(instance=settings_obj)

    context = {
        "active_tab": "settings",
        "page_title": _("Network Settings"),
        "form": form,
    }

    return render(request, "network/network_settings.html", context)


@technician_or_administrator_required
def device_group_list(request):
    """List all device groups."""
    groups = DeviceGroup.objects.annotate(device_count=Count("devices")).order_by("name")

    context = {
        "active_tab": "groups",
        "page_title": _("Device Groups"),
        "groups": groups,
    }

    return render(request, "network/device_group_list.html", context)


@administrator_required
def device_group_create(request):
    """Create a new device group."""
    if request.method == "POST":
        form = DeviceGroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            messages.success(request, _("Device group created successfully."))
            return redirect("network:device_group_list")
    else:
        form = DeviceGroupForm()

    context = {
        "active_tab": "groups",
        "page_title": _("Create Device Group"),
        "form": form,
    }

    return render(request, "network/device_group_form.html", context)


@administrator_required
def device_group_update(request, group_id):
    """Update a device group."""
    group = get_object_or_404(DeviceGroup, id=group_id)

    if request.method == "POST":
        form = DeviceGroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            messages.success(request, _("Device group updated successfully."))
            return redirect("network:device_group_list")
    else:
        form = DeviceGroupForm(instance=group)

    context = {
        "active_tab": "groups",
        "page_title": _("Update Device Group"),
        "form": form,
        "group": group,
    }

    return render(request, "network/device_group_form.html", context)


@administrator_required
def device_group_delete(request, group_id):
    """Delete a device group."""
    group = get_object_or_404(DeviceGroup, id=group_id)

    if request.method == "POST":
        group.delete()
        messages.success(request, _("Device group deleted successfully."))
        return redirect("network:device_group_list")

    context = {
        "active_tab": "groups",
        "page_title": _("Delete Device Group"),
        "group": group,
    }

    return render(request, "network/device_group_confirm_delete.html", context)


def offline_page(request):
    """Offline page for PWA - doesn't require authentication."""
    return render(request, "network/offline.html")


@technician_or_administrator_required
def analytics(request):
    """Analytics page with detailed network statistics and charts."""
    # Get traffic data for different time periods
    time_range = request.GET.get("range", "24h")

    if time_range == "7d":
        start_date = timezone.now() - timezone.timedelta(days=7)
    elif time_range == "30d":
        start_date = timezone.now() - timezone.timedelta(days=30)
    else:
        start_date = timezone.now() - timezone.timedelta(hours=24)

    traffic_logs = TrafficLog.objects.filter(timestamp__gte=start_date).order_by("timestamp")

    # Calculate statistics
    total_bandwidth = traffic_logs.aggregate(upload=Sum("upload_bytes"), download=Sum("download_bytes"))

    # Device type distribution
    device_types = Device.objects.values("device_type").annotate(count=Count("id")).order_by("-count")

    context = {
        "active_tab": "analytics",
        "page_title": _("Analytics"),
        "time_range": time_range,
        "traffic_logs": traffic_logs,
        "total_bandwidth": total_bandwidth,
        "device_types": device_types,
    }

    return render(request, "network/analytics.html", context)


@technician_or_administrator_required
def speed_test(request):
    """Speed test page to measure network performance."""
    context = {
        "active_tab": "speed_test",
        "page_title": _("Speed Test"),
    }

    return render(request, "network/speed_test.html", context)


@technician_or_administrator_required
def network_map(request):
    """Network topology visualization page."""
    devices = Device.objects.all()

    context = {
        "active_tab": "network_map",
        "page_title": _("Network Map"),
        "devices": devices,
    }

    return render(request, "network/network_map.html", context)


@administrator_required
def wifi_settings(request):
    """WiFi configuration settings page."""
    settings_obj = NetworkSettings.objects.first()

    if not settings_obj:
        settings_obj = NetworkSettings.objects.create()

    context = {
        "active_tab": "wifi_settings",
        "page_title": _("WiFi Settings"),
        "settings": settings_obj,
    }

    return render(request, "network/wifi_settings.html", context)


@administrator_required
def firewall(request):
    """Firewall rules and security settings page."""
    context = {
        "active_tab": "firewall",
        "page_title": _("Firewall"),
    }

    return render(request, "network/firewall.html", context)


@technician_or_administrator_required
def system(request):
    """System information and settings page."""
    context = {
        "active_tab": "system",
        "page_title": _("System"),
    }

    return render(request, "network/system.html", context)

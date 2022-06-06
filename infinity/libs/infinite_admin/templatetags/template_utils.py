from django import template

register = template.Library()


@register.filter
def create_tenant1_url(request):
    path = request.build_absolute_uri()
    if 'tenant1.' in path:
        pass
    elif 'tenant2.' in path:
        path = path.replace('tenant2.', 'tenant1.')
    else:
        protcol, public_url = path.split("://")
        path = protcol + '://tenant1.' + public_url
    return path


@register.filter
def create_tenant2_url(request):
    path = request.build_absolute_uri()
    if 'tenant1.' in path:
        path = path.replace('tenant1.', 'tenant2.')
    elif 'tenant2.' in path:
        pass
    else:
        protcol, public_url = path.split("://")
        path = protcol + '://tenant2.' + public_url
    return path


@register.filter
def create_public_url(request):
    path = request.build_absolute_uri()
    if 'tenant1.' in path:
        path = path.replace('tenant1.', '')
    elif 'tenant2.' in path:
        path = path.replace('tenant2.', '')
    return path

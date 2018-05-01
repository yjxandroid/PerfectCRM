# kingadmin/admin_base.py

class BaseKingAdmin(object):

    list_display = []
    list_filter = []
    search_fields = []
    #只读
    readonly_fields = []
    filter_horizontal = []
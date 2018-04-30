# kingadmin/templatetags/kingadmin_tags.py
import datetime

from django.template import Library
from django.utils.safestring import mark_safe

register = Library()

@register.simple_tag
def build_filter_ele(filter_column,admin_class):
    '''过滤功能'''
    # filter_ele = "<select name='%s'>" % filter_column
    column_obj = admin_class.model._meta.get_field(filter_column)
    try:
        filter_ele = "<select name='%s'>" % filter_column
        for choice in column_obj.get_choices():
            #默认过滤的字段没有被选中
            selected = ''
            #当前字段被过滤了
            if filter_column in admin_class.filter_conditions:
                #如果当前值被选中
                if str(choice[0]) == admin_class.filter_conditions.get(filter_column):
                    selected = 'selected'

            option = "<option value='%s' %s>%s</option>" %(choice[0],selected,choice[1])
            filter_ele += option

    except AttributeError as e:
        filter_ele = "<select name='%s__gte'>" % filter_column
        #get_internal_type():获取字段属性
        #因为时间的过滤方式是固定的（今天，过去七天，一个月.....），而不是从后台获取的
        if column_obj.get_internal_type() in ('DateField','DateTimeField'):
            time_obj = datetime.datetime.now()
            time_list = [
                ['','--------'],
                [time_obj,'Today'],
                [time_obj - datetime.timedelta(7),'七天内'],
                [time_obj.replace(day=1),'本月'],
                [time_obj - datetime.timedelta(90),'三个月内'],
                [time_obj.replace(month=1,day=1),'YearToDay(YTD)'],     #本年
                ['','ALL'],
            ]

            for i in time_list:
                selected = ''
                #因为time_list有空值（''）和时间对象，需要做个判断
                #这里运用了三元运算，if not i[0]表示为空就执行它前面的'',如果不为空则执行后面的，改变时间格式
                time_to_str = '' if not i[0] else "%s-%s-%s"%(i[0].year,i[0].month,i[0].day)
                if "%s__gte"%filter_column in admin_class.filter_conditions:
                    if time_to_str == admin_class.filter_conditions.get("%s__gte"%filter_column):
                        selected = 'selected'
                option = "<option value='%s' %s>%s</option>" %(time_to_str,selected,i[1])

                filter_ele += option

    filter_ele += "</select>"

    return mark_safe(filter_ele)


@register.simple_tag
def build_table_row(obj,admin_class):
    '''生成一条记录的html element'''

    ele = ''
    if admin_class.list_display:
        for column_name in admin_class.list_display:
            #获取所有字段对象
            column_obj = admin_class.model._meta.get_field(column_name)
            #字段对象的choices方法，如果有choices，则get_xxx_display
            if column_obj.choices:
                column_data = getattr(obj,'get_%s_display'%column_name)()
            else:
                column_data = getattr(obj,column_name)
            td_ele = "<td>%s</td>" % column_data
            ele += td_ele
    else:
        td_ele = "<td>%s</td>"%obj
        ele += td_ele

    return mark_safe(ele)

@register.simple_tag
def get_model_name(admin_class):
    '''获取表名'''
    return admin_class.model._meta.model_name.upper()

@register.simple_tag
def render_paginator(querysets):
    '''分页'''
    ele = '''
        <ul class="pagination">
    '''
    #page_range是所有的页，querysets.number是当前页
    for i in querysets.paginator.page_range:
        #显示前后三页，abs是绝对值
        if abs(querysets.number - i) < 3:
            active = ''
            if querysets.number == i:     #如果是当前页,class='active'
                active = 'active'
            p_ele = '''<li class="%s"><a href="?page=%s">%s</a></li>'''%(active,i,i)
            ele += p_ele
    ele += "</ul>"
    return mark_safe(ele)


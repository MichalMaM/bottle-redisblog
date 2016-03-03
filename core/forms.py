
def update_obj_from_form(obj, form):
    for f_name, f_val in form.data.items():
        if f_name in obj.fields:
            setattr(obj, f_name, f_val)

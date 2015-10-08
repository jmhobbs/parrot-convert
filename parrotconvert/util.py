import re

ALLOWED_FILE_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def _multiple_replacer(*key_values):
    replace_dict = dict(key_values)
    replacement_function = (lambda match: replace_dict[match.group(0)])
    pattern = re.compile("|".join([re.escape(k) for k, v in key_values]), re.M)
    return (lambda string: pattern.sub(replacement_function, string))


def multiple_replace(string, *key_values):
    return _multiple_replacer(*key_values)(string)


def is_allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_FILE_EXTENSIONS

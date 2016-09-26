class SchemaId:
    is_list = False
    id_ = None
    id_list = None

    def __init__(self, id_):
        if isinstance(id_, list):
            self.is_list = True
            self.id_list = id_
        else:
            self.id = id_

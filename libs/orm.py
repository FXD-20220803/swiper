class ModelMixin:
    def to_dict(self):
        """将 model 对象转化为 dict"""
        data = {}
        for field in self._meta.fields:
            name = field.attname
            # value = self.__dict__[name]  # 这个方法偏底层
            value = getattr(self,name)
            data[name] = value
        return data

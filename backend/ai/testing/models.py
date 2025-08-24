class TestOption():
    def __init__(self, name,is_enabled ,data):
        self.name = name
        self.is_enabled = is_enabled
        self.data = data
        
    def __str__(self):
        return f"Option: {self.name}, Enabled: {self.is_enabled}, Data: {self.data}"

class TestCase():
    def __init__(self, test_id,llm_name, embedding_model_name, system_message, chunk_size, chunk_overlap, similar_vector_count,options=None):
        self.test_id = test_id
        self.llm_name = llm_name
        self.embedding_model_name = embedding_model_name
        self.system_message = system_message
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.similar_vector_count = similar_vector_count

        self.options: list[TestOption] = []
        if options:
            self.load_options(options)
        
    def load_options(self, options):
        for option in options:
            option_obj = TestOption(option["name"], option["is_enabled"], option["data"])
            self.options.append(option_obj)
        
    def update_option(self, option_name, option_value, data):
        for option in self.options:
            if option.name == option_name:
                option.is_enabled = option_value
                option.data = data
                return
            
        option = TestOption(option_name, option_value, data)
        self.options.append(option)
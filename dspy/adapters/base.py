class Adapter:
    def __call__(self, lm, lm_kwargs, signature, demos, inputs):
        inputs = self.format(signature, demos, inputs)
        inputs = dict(prompt=inputs) if isinstance(inputs, str) else dict(messages=inputs)

        outputs = lm(**inputs, **lm_kwargs)
        values = []

        for output in outputs:
            try:
                value = self.parse(signature, output)
            except Exception as e:
                print("Failed to parse", messages, output)
                raise e
            assert set(value.keys()) == set(signature.output_fields.keys()), f"Expected {signature.output_fields.keys()} but got {value.keys()}"
            values.append(value)
        
        return values

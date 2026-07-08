class UngovernedClassifier:
    def is_ungoverned(self, event: dict) -> bool:
        return not event.get("trace_id")

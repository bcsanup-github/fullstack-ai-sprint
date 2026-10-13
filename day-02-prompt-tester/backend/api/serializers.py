from rest_framework import serializers

class PromptSerializer(serializers.Serializer):
    prompt = serializers.CharField(max_length=200)
    mode = serializers.ChoiceField(
        choices=["summarize","rewrite", "explain", "analyze"],
        default="summarize",
    )
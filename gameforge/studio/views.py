from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import GameConcept
from .services.ai_generator import generate_concept_sections

class LocalGenerateConceptView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        genre = request.data.get("genre")
        ambiance = request.data.get("ambiance")
        themes = request.data.get("themes")
        references = request.data.get("references", "")

        if not all([genre, ambiance, themes]):
            return Response({"detail": "genre, ambiance, themes sont requis."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            sections = generate_concept_sections(genre, ambiance, themes, references)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        concept = GameConcept.objects.create(
            owner=request.user,
            title="Concept sans nom",
            genre=genre,
            ambiance=ambiance,
            themes=themes,
            references=references,
            universe=sections["universe"],
            story=sections["story"],
            characters=sections["characters"],
        )

        return Response({
            "id": concept.id,
            "genre": genre,
            "ambiance": ambiance,
            "themes": themes,
            "references": references,
            **sections
        }, status=status.HTTP_201_CREATED)

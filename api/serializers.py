from rest_framework import serializers
from .models import Company, Vacancy, Resume, Application, FavoriteVacancy, Skill


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ["id", "name"]


# ============================
# VACANCY
# ============================
class VacancySerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    company_id = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.all(), source="company", write_only=True
    )
    author = serializers.StringRelatedField(read_only=True)
    salary_display = serializers.SerializerMethodField()

    class Meta:
        model = Vacancy
        fields = [
            "id",
            "title",
            "company",
            "company_id",
            "location",
            "description",
            "responsibilities",
            "requirements",
            "salary_from",
            "salary_to",
            "currency",
            "show_salary",
            "employment_type",
            "work_format",
            "experience_required",
            "is_active",
            "views",
            "created_at",
            "updated_at",
            "author",
            "salary_display",
        ]

    def get_salary_display(self, obj):
        return obj.salary_display()


# ============================
# RESUME
# ============================
class ResumeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    skills = SkillSerializer(many=True, read_only=True)
    skill_ids = serializers.PrimaryKeyRelatedField(
        queryset=Skill.objects.all(), many=True, source="skills", write_only=True
    )

    class Meta:
        model = Resume
        fields = [
            "id",
            "user",
            "full_name",
            "desired_position",
            "location",
            "phone",
            "email",
            "salary_expectation",
            "experience_years",
            "about",
            "skills",
            "skill_ids",
            "is_active",
            "created_at",
            "updated_at",
        ]


# ============================
# APPLICATION (Response)
# ============================
class ApplicationSerializer(serializers.ModelSerializer):
    applicant = serializers.StringRelatedField(read_only=True)
    vacancy = serializers.StringRelatedField(read_only=True)
    resume = ResumeSerializer(read_only=True)
    resume_id = serializers.PrimaryKeyRelatedField(
        queryset=Resume.objects.all(), source="resume", write_only=True, required=False
    )

    class Meta:
        model = Application
        fields = [
            "id",
            "applicant",
            "vacancy",
            "resume",
            "resume_id",
            "cover_letter",
            "status",
            "applied_at",
            "updated_at",
        ]


# ============================
# FAVORITES
# ============================
class FavoriteVacancySerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    vacancy = VacancySerializer(read_only=True)
    vacancy_id = serializers.PrimaryKeyRelatedField(
        queryset=Vacancy.objects.all(), source="vacancy", write_only=True
    )

    class Meta:
        model = FavoriteVacancy
        fields = ["id", "user", "vacancy", "vacancy_id", "added_at"]


class FavoriteToggleResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
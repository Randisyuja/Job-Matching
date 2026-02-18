from django.utils import timezone


class LowonganService:

    @staticmethod
    def create_lowongan(*, data, user):
        data["created_by"] = user
        data["updated_by"] = user
        data["created_at"] = timezone.now()
        data["updated_at"] = timezone.now()
        return data

    @staticmethod
    def update_lowongan(*, instance, data, user):
        data["updated_by"] = user
        data["updated_at"] = timezone.now()
        return data

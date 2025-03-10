from groovetimeapi.models import GrooveSubmission, GroovetimeUser


def update_user_groove_points(user):

    user_submissions = GrooveSubmission.objects.filter(submitted_by=user)
    total_average_ratings = sum(
        sub.average_rating for sub in user_submissions if sub.average_rating is not None)

    grooves_won_bonus = user.grooves_won * 10

    user.groove_points = total_average_ratings + grooves_won_bonus
    user.save()

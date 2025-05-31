from ninja import NinjaAPI
from user.api import router as user_router
from content.api import router as content_router
from comment.api import router as comment_router
from recommendation.api import router as recommendation_router
from discussion.api import router as discussion_router

api = NinjaAPI(csrf=True , title="Mentora+ API", version="1.0")

api.add_router("/user/", user_router)
api.add_router("/content/", content_router)
api.add_router("/comment/", comment_router)
api.add_router("/recommendation/", recommendation_router)
api.add_router("/discussion/", discussion_router)

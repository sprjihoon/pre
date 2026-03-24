import api from "./client";

export const llmApi = {
  review: (recommendationIds: number[], reviewLevel = "light") =>
    api.post("/llm/review", { recommendation_ids: recommendationIds, review_level: reviewLevel }),
  reviews: (recommendationId?: number, reviewType?: string) =>
    api.get("/llm/reviews", { params: { recommendation_id: recommendationId, review_type: reviewType } }),
};

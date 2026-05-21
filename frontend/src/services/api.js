import axios from "axios";

const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL,
});

export default API;

export const loadData = () => API.post("/data/load");

export const exploreData = () => API.get("/data/explore");

export const preprocessData = () =>
  API.post("/data/preprocess", {
    test_size: 0.2,
    random_state: 42,
  });

export const trainModel = (modelType) =>
  API.post("/models/train", {
    model_type: modelType,
    random_state: 42,
  });

export const generatePredictions = () =>
  API.post("/predictions/predict");

export const getMetrics = () =>
  API.get("/evaluation/metrics");

export const getQini = () =>
  API.get("/evaluation/qini");

export const getDeciles = () =>
  API.get("/evaluation/deciles");

export const getComparison = () =>
  API.get("/evaluation/comparison");

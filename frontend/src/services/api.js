import axios from "axios";

const API = axios.create({
  baseURL: process.env.REACT_APP_API_URL,
});

export default API;

// ================= DATA =================

export const loadData = () =>
  API.post("/api/v1/data/load");

export const exploreData = () =>
  API.get("/api/v1/data/explore");

export const preprocessData = () =>
  API.post("/api/v1/data/preprocess", {
    test_size: 0.2,
    random_state: 42,
  });

// ================= TRAINING =================

export const trainModel = (modelType) =>
  API.post("/api/v1/models/train", {
    model_type: modelType,
    random_state: 42,
  });

// ================= PREDICTIONS =================

export const generatePredictions = () =>
  API.post("/api/v1/predictions/predict");

// ================= EVALUATION =================

export const getMetrics = () =>
  API.get("/api/v1/evaluation/metrics");

export const getQini = () =>
  API.get("/api/v1/evaluation/qini");

export const getDeciles = () =>
  API.get("/api/v1/evaluation/deciles");

export const getComparison = () =>
  API.get("/api/v1/evaluation/comparison");

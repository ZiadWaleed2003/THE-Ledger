import { Asset } from "@/types/asset";

const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

export async function fetchAssets(): Promise<Asset[]> {
  const response = await fetch(`${API_BASE}/assets/`);
  if (!response.ok) {
    throw new Error("Failed to fetch assets");
  }
  return response.json();
}

export async function createAsset(asset: Omit<Asset, "id">): Promise<Asset> {
  const response = await fetch(`${API_BASE}/assets/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(asset),
  });
  if (!response.ok) {
    throw new Error("Failed to create asset");
  }
  return response.json();
}

export async function updateAsset(id: string, asset: Omit<Asset, "id">): Promise<Asset> {
  const response = await fetch(`${API_BASE}/assets/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(asset),
  });
  if (!response.ok) {
    throw new Error("Failed to update asset");
  }
  return response.json();
}

export async function deleteAsset(id: string): Promise<void> {
  const response = await fetch(`${API_BASE}/assets/${id}`, {
    method: "DELETE",
  });
  if (!response.ok) {
    throw new Error("Failed to delete asset");
  }
}

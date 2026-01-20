import { useState, useEffect } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { Plus, Pencil, Trash2, Package, Loader2 } from "lucide-react";
import { format } from "date-fns";

import { Asset } from "@/types/asset";
import { fetchAssets, createAsset, updateAsset, deleteAsset } from "@/lib/api";

import { Button } from "@/components/ui/button";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@/components/ui/alert-dialog";
import { AssetFormDialog } from "@/components/AssetFormDialog";
import { useToast } from "@/hooks/use-toast";

export default function AssetRegistry() {
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [editingAsset, setEditingAsset] = useState<Asset | null>(null);
  const [deletingAsset, setDeletingAsset] = useState<Asset | null>(null);
  const { toast } = useToast();
  const queryClient = useQueryClient();

  const { data: assets, isLoading, error } = useQuery({
    queryKey: ["assets"],
    queryFn: fetchAssets,
  });

  const createMutation = useMutation({
    mutationFn: createAsset,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["assets"] });
      toast({ title: "Asset created successfully" });
      setIsFormOpen(false);
    },
    onError: () => {
      toast({ title: "Failed to create asset", variant: "destructive" });
    },
  });

  const updateMutation = useMutation({
    mutationFn: ({ id, data }: { id: string; data: Omit<Asset, "id"> }) =>
      updateAsset(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["assets"] });
      toast({ title: "Asset updated successfully" });
      setEditingAsset(null);
    },
    onError: () => {
      toast({ title: "Failed to update asset", variant: "destructive" });
    },
  });

  const deleteMutation = useMutation({
    mutationFn: deleteAsset,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["assets"] });
      toast({ title: "Asset deleted successfully" });
      setDeletingAsset(null);
    },
    onError: () => {
      toast({ title: "Failed to delete asset", variant: "destructive" });
    },
  });

  const handleSubmit = (data: Omit<Asset, "id">) => {
    if (editingAsset) {
      updateMutation.mutate({ id: editingAsset.id, data });
    } else {
      createMutation.mutate(data);
    }
  };

  const getStatusVariant = (status: Asset["status"]) => {
    switch (status) {
      case "Active":
        return "default";
      case "Maintenance":
        return "secondary";
      case "Retired":
        return "outline";
      default:
        return "default";
    }
  };

  return (
    <div className="flex flex-col h-full">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-semibold text-foreground">Asset Registry</h1>
          <p className="text-muted-foreground mt-1">
            Manage and track all your organization's assets
          </p>
        </div>
        <Button onClick={() => setIsFormOpen(true)}>
          <Plus className="mr-2 h-4 w-4" />
          Add New Asset
        </Button>
      </div>

      <div className="flex-1 border border-border rounded-lg overflow-hidden bg-card">
        {isLoading ? (
          <div className="flex items-center justify-center h-64">
            <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
          </div>
        ) : error ? (
          <div className="flex flex-col items-center justify-center h-64 text-muted-foreground">
            <Package className="h-12 w-12 mb-4 opacity-50" />
            <p className="text-lg font-medium">Unable to load assets</p>
            <p className="text-sm">Make sure your backend is running at {import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000"}</p>
          </div>
        ) : !assets || assets.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-64 text-muted-foreground">
            <Package className="h-12 w-12 mb-4 opacity-50" />
            <p className="text-lg font-medium">No assets found</p>
            <p className="text-sm">Add your first asset to get started</p>
          </div>
        ) : (
          <Table>
            <TableHeader>
              <TableRow className="bg-muted/30 hover:bg-muted/30">
                <TableHead className="font-semibold">Name</TableHead>
                <TableHead className="font-semibold">Category</TableHead>
                <TableHead className="font-semibold">Value</TableHead>
                <TableHead className="font-semibold">Status</TableHead>
                <TableHead className="font-semibold">Purchase Date</TableHead>
                <TableHead className="font-semibold w-[100px]">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {assets.map((asset) => (
                <TableRow key={asset.id} className="hover:bg-muted/20">
                  <TableCell className="font-medium">{asset.name}</TableCell>
                  <TableCell>{asset.category}</TableCell>
                  <TableCell>
                    ${asset.value.toLocaleString("en-US", { minimumFractionDigits: 2 })}
                  </TableCell>
                  <TableCell>
                    <Badge variant={getStatusVariant(asset.status)}>
                      {asset.status}
                    </Badge>
                  </TableCell>
                  <TableCell>
                    {format(new Date(asset.purchase_date), "MMM dd, yyyy")}
                  </TableCell>
                  <TableCell>
                    <div className="flex items-center gap-2">
                      <Button
                        variant="ghost"
                        size="icon"
                        onClick={() => setEditingAsset(asset)}
                      >
                        <Pencil className="h-4 w-4" />
                      </Button>
                      <Button
                        variant="ghost"
                        size="icon"
                        onClick={() => setDeletingAsset(asset)}
                      >
                        <Trash2 className="h-4 w-4 text-destructive" />
                      </Button>
                    </div>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        )}
      </div>

      <AssetFormDialog
        open={isFormOpen || !!editingAsset}
        onOpenChange={(open) => {
          if (!open) {
            setIsFormOpen(false);
            setEditingAsset(null);
          }
        }}
        asset={editingAsset}
        onSubmit={handleSubmit}
        isLoading={createMutation.isPending || updateMutation.isPending}
      />

      <AlertDialog open={!!deletingAsset} onOpenChange={() => setDeletingAsset(null)}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Delete Asset</AlertDialogTitle>
            <AlertDialogDescription>
              Are you sure you want to delete "{deletingAsset?.name}"? This action cannot be undone.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Cancel</AlertDialogCancel>
            <AlertDialogAction
              onClick={() => deletingAsset && deleteMutation.mutate(deletingAsset.id)}
              className="bg-destructive text-destructive-foreground hover:bg-destructive/90"
            >
              {deleteMutation.isPending ? (
                <Loader2 className="h-4 w-4 animate-spin" />
              ) : (
                "Delete"
              )}
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </div>
  );
}

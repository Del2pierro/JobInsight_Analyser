"use client";

import { useState } from "react";
import DashboardLayout from "@/components/layout/DashboardLayout";
import { UploadCloud, FileText, CheckCircle, AlertCircle } from "lucide-react";
import api from "@/lib/axios";

export default function ResumesPage() {
  const [file, setFile] = useState<File | null>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState<"idle" | "success" | "error">("idle");
  const [errorMessage, setErrorMessage] = useState("");

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const droppedFile = e.dataTransfer.files[0];
      if (droppedFile.type === "application/pdf") {
        setFile(droppedFile);
        setUploadStatus("idle");
      } else {
        setUploadStatus("error");
        setErrorMessage("Veuillez déposer un fichier PDF uniquement.");
      }
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const selectedFile = e.target.files[0];
      if (selectedFile.type === "application/pdf") {
        setFile(selectedFile);
        setUploadStatus("idle");
      } else {
        setUploadStatus("error");
        setErrorMessage("Veuillez sélectionner un fichier PDF uniquement.");
      }
    }
  };

  const handleUpload = async () => {
    if (!file) return;

    setIsUploading(true);
    setUploadStatus("idle");
    setErrorMessage("");

    const formData = new FormData();
    formData.append("file", file);

    try {
      // Send multipart/form-data to the backend
      await api.post("/resumes/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" }
      });

      setUploadStatus("success");
      setFile(null); // Reset form
    } catch (err: any) {
      setUploadStatus("error");
      setErrorMessage(err.response?.data?.detail || "Erreur lors du téléchargement. Veuillez réessayer.");
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <DashboardLayout>
      <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
        <div>
          <h2 className="text-3xl font-bold tracking-tight">Vos CVs</h2>
          <p className="text-muted-foreground mt-1">
            Déposez votre CV au format PDF. Notre IA extraira automatiquement vos compétences pour les faire correspondre au marché.
          </p>
        </div>

        <div className="grid gap-8 md:grid-cols-2">

          {/* Zone d'Upload (Drag & Drop) */}
          <div className="rounded-xl border bg-card text-card-foreground shadow-sm p-8 glass-panel hover-lift">
            <h3 className="font-semibold text-lg mb-4">Télécharger un nouveau CV</h3>

            <div
              className={`border-2 border-dashed rounded-xl p-10 flex flex-col items-center justify-center text-center transition-all duration-300 ${isDragging
                  ? "border-primary bg-primary/10 scale-[1.02]"
                  : "border-muted-foreground/30 hover:border-primary/50 hover:bg-muted/10"
                }`}
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              onDrop={handleDrop}
            >
              <UploadCloud className={`h-12 w-12 mb-4 transition-colors ${isDragging ? "text-primary" : "text-muted-foreground"}`} />

              <h4 className="text-base font-medium mb-2 text-foreground">
                Glissez & Déposez votre PDF ici
              </h4>
              <p className="text-sm text-muted-foreground mb-6">
                Taille maximale : 5 MB
              </p>

              <label className="cursor-pointer bg-primary text-primary-foreground px-4 py-2.5 rounded-md text-sm font-semibold hover:bg-primary/90 transition-colors shadow-sm">
                <span>Parcourir mes fichiers</span>
                <input
                  type="file"
                  className="hidden"
                  accept=".pdf,application/pdf"
                  onChange={handleFileChange}
                />
              </label>
            </div>

            {/* Fichier sélectionné en attente d'upload */}
            {file && uploadStatus !== "success" && (
              <div className="mt-6 p-4 rounded-lg border bg-muted/30 flex items-center justify-between animate-in slide-in-from-top-2">
                <div className="flex items-center gap-3 overflow-hidden">
                  <div className="p-2 bg-primary/20 text-primary rounded-md">
                    <FileText size={20} />
                  </div>
                  <div className="truncate">
                    <p className="text-sm font-medium truncate">{file.name}</p>
                    <p className="text-xs text-muted-foreground">{(file.size / 1024 / 1024).toFixed(2)} MB</p>
                  </div>
                </div>
                <button
                  onClick={handleUpload}
                  disabled={isUploading}
                  className="ml-4 bg-foreground text-background px-4 py-2 rounded-md text-sm font-medium hover:bg-foreground/80 disabled:opacity-50 transition-colors"
                >
                  {isUploading ? "Analyse IA..." : "Analyser ce CV"}
                </button>
              </div>
            )}

            {/* Messages de statut */}
            {uploadStatus === "success" && (
              <div className="mt-6 p-4 rounded-lg bg-green-500/10 border border-green-500/20 flex items-center gap-3 animate-in slide-in-from-top-2 text-green-600 dark:text-green-400">
                <CheckCircle className="h-5 w-5" />
                <p className="text-sm font-medium">CV reçu avec succès ! L'IA est en cours d'extraction en arrière-plan.</p>
              </div>
            )}

            {uploadStatus === "error" && (
              <div className="mt-6 p-4 rounded-lg bg-destructive/10 border border-destructive/20 flex items-center gap-3 animate-in slide-in-from-top-2 text-destructive">
                <AlertCircle className="h-5 w-5" />
                <p className="text-sm font-medium">{errorMessage}</p>
              </div>
            )}
          </div>

          {/* Liste des CVs précédents (Mockup visuel pour l'instant) */}
          <div className="rounded-xl border bg-card text-card-foreground shadow-sm p-8 glass-panel hover-lift">
            <h3 className="font-semibold text-lg mb-4">Historique de vos CVs</h3>

            <div className="space-y-4">
              {/* Exemple de CV traité */}
              <div className="p-4 rounded-lg border bg-background flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="p-2 bg-primary/20 text-primary rounded-md">
                    <FileText size={20} />
                  </div>
                  <div>
                    <p className="text-sm font-medium">CV_Pierre_Dupont_2026.pdf</p>
                    <div className="flex items-center gap-2 mt-1">
                      <span className="flex h-2 w-2 rounded-full bg-green-500"></span>
                      <p className="text-xs text-muted-foreground">Analysé par l'IA • il y a 2 jours</p>
                    </div>
                  </div>
                </div>
                <div className="text-xs font-semibold text-primary bg-primary/10 px-2 py-1 rounded">
                  Actif
                </div>
              </div>

              {/* Message de chargement / état vide */}
              <div className="p-8 text-center text-muted-foreground border-2 border-dashed rounded-lg">
                <p className="text-sm">Bientôt : la liste complète chargée depuis l'API.</p>
              </div>
            </div>
          </div>

        </div>
      </div>
    </DashboardLayout>
  );
}

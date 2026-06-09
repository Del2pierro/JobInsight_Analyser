"use client";

import { useState, useEffect, useCallback } from "react";
import DashboardLayout from "@/components/layout/DashboardLayout";
import {
  Briefcase, MapPin, Building, Calendar, Star, Search,
  CheckCircle, Globe, ExternalLink, RefreshCw, Bot
} from "lucide-react";
import api from "@/lib/axios";

// -----------------------------------------------------------------------
// Interfaces TypeScript (strict: true — pas de any)
// -----------------------------------------------------------------------

interface Job {
  id: string;
  title: string;
  company: string;
  location: string;
  description: string;
  raw_url?: string;
  status: string;
  source?: string;
  created_at: string;
}

export default function JobsPage() {
  // --- State ---
  const [jobs, setJobs] = useState<Job[]>([]);
  const [selectedJob, setSelectedJob] = useState<Job | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [searchFilter, setSearchFilter] = useState("");

  // -----------------------------------------------------------------------
  // Chargement des offres depuis le backend
  // -----------------------------------------------------------------------
  const fetchJobs = useCallback(async () => {
    setIsLoading(true);
    try {
      const res = await api.get("/jobs/");
      setJobs(res.data);
      if (res.data.length > 0 && !selectedJob) {
        setSelectedJob(res.data[0]);
      }
    } catch (err) {
      console.error("Erreur de récupération des jobs:", err);
    } finally {
      setIsLoading(false);
    }
  }, [selectedJob]);

  useEffect(() => {
    fetchJobs();
  }, [fetchJobs]);

  // -----------------------------------------------------------------------
  // Filtrer les offres par la barre de recherche
  // -----------------------------------------------------------------------
  const filteredJobs = jobs.filter(
    (job) =>
      job.title.toLowerCase().includes(searchFilter.toLowerCase()) ||
      job.company.toLowerCase().includes(searchFilter.toLowerCase()) ||
      (job.location && job.location.toLowerCase().includes(searchFilter.toLowerCase()))
  );

  // -----------------------------------------------------------------------
  // Formater une date ISO en "12 juin 2026"
  // -----------------------------------------------------------------------
  const formatDate = (dateStr: string) => {
    try {
      return new Date(dateStr).toLocaleDateString("fr-FR", {
        day: "numeric",
        month: "short",
        year: "numeric",
      });
    } catch {
      return "Date inconnue";
    }
  };

  return (
    <DashboardLayout>
      <div className="h-[calc(100vh-8rem)] flex flex-col space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
        {/* ============================================================= */}
        {/* En-tête : titre + badge source + refresh */}
        {/* ============================================================= */}
        <div className="flex justify-between items-end">
          <div>
            <h2 className="text-3xl font-bold tracking-tight">
              Offres d&apos;emploi
            </h2>
            <p className="text-muted-foreground mt-1">
              Collectées automatiquement depuis Remotive · Mises à jour toutes les 6h
            </p>
          </div>

          <div className="flex items-center gap-3">
            {/* Badge informatif */}
            <span className="flex items-center gap-1.5 text-xs bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 px-3 py-1.5 rounded-full font-medium">
              <Bot size={14} />
              Scraping auto actif
            </span>

            {/* Bouton refresh manuel */}
            <button
              onClick={fetchJobs}
              disabled={isLoading}
              className="flex items-center gap-2 bg-secondary text-secondary-foreground border px-4 py-2 rounded-lg text-sm font-medium hover:bg-accent transition-all disabled:opacity-50"
            >
              <RefreshCw size={16} className={isLoading ? "animate-spin" : ""} />
              Actualiser
            </button>
          </div>
        </div>

        {/* ============================================================= */}
        {/* Layout Master/Detail */}
        {/* ============================================================= */}
        <div className="flex gap-6 flex-1 min-h-0">
          {/* --- Panneau gauche : Liste des offres --- */}
          <div className="w-1/3 flex flex-col gap-4">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground h-4 w-4" />
              <input
                id="job-search-input"
                type="text"
                placeholder="Rechercher une offre..."
                value={searchFilter}
                onChange={(e) => setSearchFilter(e.target.value)}
                className="w-full pl-9 pr-4 py-2 bg-card border rounded-lg text-sm focus:outline-none focus:ring-1 focus:ring-primary transition-shadow"
              />
            </div>

            <div className="flex-1 overflow-y-auto space-y-3 pr-2 custom-scrollbar">
              {isLoading ? (
                <div className="text-center p-8 text-muted-foreground animate-pulse">
                  Chargement des offres...
                </div>
              ) : filteredJobs.length === 0 ? (
                <div className="text-center p-8 border border-dashed rounded-lg text-muted-foreground bg-muted/10">
                  <Bot size={40} className="mx-auto mb-3 opacity-30" />
                  <p className="font-medium">Aucune offre disponible</p>
                  <p className="text-xs mt-1">
                    Le scraping automatique collectera des offres prochainement.
                  </p>
                </div>
              ) : (
                filteredJobs.map((job) => (
                  <div
                    key={job.id}
                    onClick={() => setSelectedJob(job)}
                    className={`p-4 rounded-xl border cursor-pointer transition-all duration-200 ${
                      selectedJob?.id === job.id
                        ? "border-primary bg-primary/5 shadow-md scale-[1.02]"
                        : "bg-card hover:border-primary/50 hover:bg-accent/50"
                    }`}
                  >
                    <div className="flex items-start justify-between">
                      <h3 className="font-semibold text-foreground truncate flex-1">
                        {job.title}
                      </h3>
                      {job.source && (
                        <span className="text-[10px] bg-primary/20 text-primary px-2 py-0.5 rounded-full font-bold ml-2 shrink-0 capitalize">
                          {job.source}
                        </span>
                      )}
                    </div>
                    <p className="text-sm text-primary font-medium mt-1 truncate">
                      {job.company}
                    </p>
                    <div className="flex items-center gap-3 mt-3 text-xs text-muted-foreground">
                      <span className="flex items-center gap-1">
                        <MapPin size={12} /> {job.location || "Non spécifié"}
                      </span>
                      <span className="flex items-center gap-1">
                        <Calendar size={12} /> {formatDate(job.created_at)}
                      </span>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>

          {/* --- Panneau droit : Détails du Job sélectionné --- */}
          <div className="flex-1 rounded-xl border bg-card shadow-sm p-8 glass-panel flex flex-col overflow-hidden">
            {selectedJob ? (
              <div className="h-full flex flex-col">
                {/* Header */}
                <div className="border-b pb-6 mb-6">
                  <div className="flex justify-between items-start">
                    <div className="pr-4 flex-1">
                      <h2 className="text-2xl font-bold leading-tight">
                        {selectedJob.title}
                      </h2>
                      <div className="flex flex-wrap items-center gap-4 mt-3 text-muted-foreground text-sm">
                        <span className="flex items-center gap-1.5 text-primary font-medium">
                          <Building size={16} /> {selectedJob.company}
                        </span>
                        <span className="flex items-center gap-1.5">
                          <MapPin size={16} />{" "}
                          {selectedJob.location || "Non spécifié"}
                        </span>
                        <span className="flex items-center gap-1.5">
                          <Calendar size={16} />{" "}
                          {formatDate(selectedJob.created_at)}
                        </span>
                        {selectedJob.source && (
                          <span className="flex items-center gap-1.5 text-primary capitalize">
                            <Globe size={16} /> Scrapée via {selectedJob.source}
                          </span>
                        )}
                      </div>
                    </div>

                    {/* Badge Score IA — sera connecté au vrai score Qdrant */}
                    <div className="bg-primary/10 border border-primary/20 text-primary px-5 py-3 rounded-xl flex flex-col items-center justify-center shrink-0 shadow-inner">
                      <div className="text-xs font-bold uppercase tracking-wider opacity-80 mb-1">
                        Score IA
                      </div>
                      <div className="text-3xl font-extrabold">—</div>
                    </div>
                  </div>
                </div>

                {/* Actions */}
                <div className="flex gap-4 mb-8">
                  <button
                    id="btn-match-cv"
                    className="flex-1 bg-primary text-primary-foreground py-2.5 rounded-lg text-sm font-semibold hover:bg-primary/90 transition-colors shadow-sm flex items-center justify-center gap-2"
                  >
                    <CheckCircle size={18} />
                    Lancer le Matching avec mon CV
                  </button>
                  {selectedJob.raw_url && (
                    <a
                      href={selectedJob.raw_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="bg-secondary text-secondary-foreground border py-2.5 px-6 rounded-lg text-sm font-semibold hover:bg-accent transition-colors flex items-center justify-center gap-2"
                    >
                      <ExternalLink size={18} /> Voir l&apos;offre
                    </a>
                  )}
                  <button
                    id="btn-save-job"
                    className="bg-secondary text-secondary-foreground border py-2.5 px-6 rounded-lg text-sm font-semibold hover:bg-accent transition-colors flex items-center justify-center gap-2"
                  >
                    <Star size={18} /> Sauvegarder
                  </button>
                </div>

                {/* Contenu scrollable */}
                <div className="flex-1 overflow-y-auto pr-4 custom-scrollbar space-y-8">
                  {/* Compétences extraites par l'Agent NLP */}
                  <div>
                    <h3 className="font-semibold mb-4 flex items-center gap-2 text-foreground">
                      <Briefcase size={18} className="text-primary" />
                      Compétences extraites (Agent NLP spaCy)
                    </h3>
                    <div className="flex flex-wrap gap-2.5">
                      {/* TODO: Connecter aux vraies compétences extraites par l'Agent Extractor */}
                      <span className="text-sm text-muted-foreground italic">
                        Les compétences seront extraites automatiquement par l&apos;agent NLP.
                      </span>
                    </div>
                  </div>

                  {/* Description originale */}
                  <div>
                    <h3 className="font-semibold mb-3 text-foreground border-b pb-2">
                      Description de l&apos;offre
                    </h3>
                    <div className="text-sm text-muted-foreground leading-relaxed whitespace-pre-wrap bg-muted/20 p-5 rounded-xl border border-muted/50">
                      {selectedJob.description ||
                        "Aucune description disponible pour cette offre."}
                    </div>
                  </div>
                </div>
              </div>
            ) : (
              <div className="h-full flex flex-col items-center justify-center text-muted-foreground opacity-60">
                <Briefcase size={80} className="mb-6 opacity-20" />
                <p className="text-lg font-medium text-foreground">
                  Sélectionnez une offre
                </p>
                <p className="text-sm mt-1">
                  L&apos;IA de JobInsight l&apos;analysera instantanément.
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}

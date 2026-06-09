"use client";

import { useState, useEffect } from "react";
import DashboardLayout from "@/components/layout/DashboardLayout";
import { 
  FileText, 
  Download, 
  Plus, 
  Clock, 
  CheckCircle, 
  AlertCircle, 
  Loader2,
  FileSearch,
  Zap,
  Briefcase
} from "lucide-react";
import api from "@/lib/axios";

interface Report {
  id: string;
  title: string;
  type: "market_analysis" | "skill_gap" | "interview_prep";
  status: "processing" | "ready" | "failed";
  created_at: string;
  url?: string;
}

export default function ReportsPage() {
  const [reports, setReports] = useState<Report[]>([]);
  const [loading, setLoading] = useState(true);
  const [isGenerating, setIsGenerating] = useState(false);

  useEffect(() => {
    const fetchReports = async () => {
      try {
        const response = await api.get("/reports/");
        setReports(response.data);
      } catch (error) {
        console.error("Failed to fetch reports:", error);
        setReports([]);
      } finally {
        setLoading(false);
      }
    };

    fetchReports();
  }, []);

  const handleGenerateReport = async (type: string) => {
    setIsGenerating(true);
    try {
      // API call to ReportAgent
      // await api.post("/reports/generate", { type });
      // For now, just simulate
      setTimeout(() => setIsGenerating(false), 2000);
    } catch (error) {
      console.error("Generation failed:", error);
      setIsGenerating(false);
    }
  };

  return (
    <DashboardLayout>
      <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
        <div>
          <h2 className="text-3xl font-bold tracking-tight">Rapports & Analyses</h2>
          <p className="text-muted-foreground mt-1">
            Générez des synthèses PDF personnalisées grâce à nos agents IA pour booster votre recherche d&apos;emploi.
          </p>
        </div>

        {/* Action Cards */}
        <div className="grid gap-6 md:grid-cols-3">
          <ReportTypeCard 
            title="Analyse de Marché"
            description="Vue d'ensemble des salaires et de la demande pour votre profil."
            icon={<FileSearch className="text-blue-500" />}
            onClick={() => handleGenerateReport("market_analysis")}
            disabled={isGenerating}
          />
          <ReportTypeCard 
            title="Skill Gap Analysis"
            description="Identifiez les compétences manquantes pour vos jobs cibles."
            icon={<Zap className="text-amber-500" />}
            onClick={() => handleGenerateReport("skill_gap")}
            disabled={isGenerating}
          />
          <ReportTypeCard 
            title="Préparation Entretien"
            description="Questions types et conseils basés sur une offre spécifique."
            icon={<Briefcase className="text-purple-500" />}
            onClick={() => handleGenerateReport("interview_prep")}
            disabled={isGenerating}
          />
        </div>

        {/* Reports List */}
        <div className="rounded-2xl border bg-card shadow-sm overflow-hidden">
          <div className="p-6 border-b bg-muted/30">
            <h3 className="font-bold text-lg">Historique des rapports</h3>
          </div>
          
          <div className="divide-y">
            {loading ? (
              <div className="p-12 flex justify-center">
                <Loader2 className="h-8 w-8 animate-spin text-primary opacity-50" />
              </div>
            ) : reports.length > 0 ? (
              reports.map((report) => (
                <ReportRow key={report.id} report={report} />
              ))
            ) : (
              <div className="p-12 text-center text-muted-foreground">
                <FileText size={48} className="mx-auto mb-4 opacity-20" />
                <p>Vous n&apos;avez pas encore généré de rapport.</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}

function ReportTypeCard({ title, description, icon, onClick, disabled }: any) {
  return (
    <div className="rounded-xl border bg-card p-6 shadow-sm hover-lift transition-all flex flex-col items-start gap-4">
      <div className="p-3 bg-muted rounded-lg border">
        {icon}
      </div>
      <div>
        <h4 className="font-bold text-foreground">{title}</h4>
        <p className="text-xs text-muted-foreground mt-1 leading-relaxed">
          {description}
        </p>
      </div>
      <button 
        onClick={onClick}
        disabled={disabled}
        className="mt-2 w-full flex items-center justify-center gap-2 bg-secondary text-secondary-foreground py-2 rounded-lg text-sm font-semibold hover:bg-accent transition-colors disabled:opacity-50"
      >
        <Plus size={16} />
        Générer
      </button>
    </div>
  );
}

function ReportRow({ report }: { report: Report }) {
  const formatDate = (dateStr: string) => {
    return new Date(dateStr).toLocaleDateString("fr-FR", {
      day: "numeric",
      month: "long",
      year: "numeric"
    });
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case "ready": return <CheckCircle size={18} className="text-green-500" />;
      case "processing": return <Clock size={18} className="text-amber-500 animate-pulse" />;
      case "failed": return <AlertCircle size={18} className="text-destructive" />;
      default: return null;
    }
  };

  return (
    <div className="p-4 sm:p-6 flex flex-col sm:flex-row sm:items-center justify-between gap-4 hover:bg-muted/10 transition-colors">
      <div className="flex items-center gap-4">
        <div className="p-3 bg-primary/10 text-primary rounded-xl hidden sm:block">
          <FileText size={24} />
        </div>
        <div>
          <h4 className="font-semibold text-foreground">{report.title}</h4>
          <p className="text-xs text-muted-foreground mt-1">
            Généré le {formatDate(report.created_at)}
          </p>
        </div>
      </div>

      <div className="flex items-center justify-between sm:justify-end gap-6">
        <div className="flex items-center gap-2 text-sm font-medium">
          {getStatusIcon(report.status)}
          <span className="capitalize">
            {report.status === "ready" ? "Prêt" : report.status === "processing" ? "En cours..." : "Échec"}
          </span>
        </div>

        {report.status === "ready" && (
          <a 
            href={report.url}
            className="flex items-center gap-2 text-primary hover:text-primary/80 font-bold text-sm transition-colors"
          >
            <Download size={18} />
            <span className="hidden sm:inline">Télécharger PDF</span>
          </a>
        )}
      </div>
    </div>
  );
}

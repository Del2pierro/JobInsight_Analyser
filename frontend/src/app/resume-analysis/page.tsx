"use client";

import { useState, useEffect } from "react";
import DashboardLayout from "@/components/layout/DashboardLayout";
import { 
  FileText, 
  Target, 
  Sparkles, 
  ArrowRight, 
  Trophy, 
  AlertCircle,
  CheckCircle2,
  Lightbulb,
  Loader2
} from "lucide-react";
import api from "@/lib/axios";

interface AnalysisResult {
  score: number;
  top_matches: Array<{ id: string; title: string; company: string; match_score: number }>;
  recommendations: string[];
  missing_skills: string[];
  strengths: string[];
}

export default function ResumeAnalysisPage() {
  const [analysis, setAnalysis] = useState<AnalysisResult | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAnalysis = async () => {
      try {
        const response = await api.get("/matching/resume-analysis");
        setAnalysis(response.data);
      } catch (error) {
        console.error("Failed to fetch analysis:", error);
        setAnalysis(null);
      } finally {
        setLoading(false);
      }
    };

    fetchAnalysis();
  }, []);

  if (loading) {
    return (
      <DashboardLayout>
        <div className="flex h-[70vh] items-center justify-center">
          <Loader2 className="h-12 w-12 animate-spin text-primary opacity-50" />
        </div>
      </DashboardLayout>
    );
  }

  if (!analysis) {
    return (
      <DashboardLayout>
        <div className="flex flex-col h-[70vh] items-center justify-center text-center p-8">
          <AlertCircle className="h-12 w-12 text-muted-foreground mb-4 opacity-20" />
          <h2 className="text-xl font-bold mb-2">Aucune analyse disponible</h2>
          <p className="text-muted-foreground max-w-md">
            Téléchargez un CV dans la section "Mes CVs" pour lancer une analyse approfondie de votre profil.
          </p>
        </div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
        <div className="flex justify-between items-end">
          <div>
            <h2 className="text-3xl font-bold tracking-tight">Analyse Approfondie du CV</h2>
            <p className="text-muted-foreground mt-1">
              Résultats générés par le CVMatchingAgent et le CareerAdvisorAgent.
            </p>
          </div>
          <div className="hidden md:block text-sm text-muted-foreground bg-muted px-4 py-2 rounded-lg border">
            Dernière analyse : 09 juin 2026
          </div>
        </div>

        {/* Global Score & Top Matches */}
        <div className="grid gap-6 lg:grid-cols-3">
          
          {/* Main Score Card */}
          <div className="lg:col-span-1 rounded-2xl border bg-card p-8 shadow-sm flex flex-col items-center justify-center text-center glass-panel">
            <div className="relative h-40 w-40 flex items-center justify-center mb-6">
              <svg className="h-full w-full rotate-[-90deg]">
                <circle
                  cx="80"
                  cy="80"
                  r="70"
                  stroke="currentColor"
                  strokeWidth="10"
                  fill="transparent"
                  className="text-muted/30"
                />
                <circle
                  cx="80"
                  cy="80"
                  r="70"
                  stroke="currentColor"
                  strokeWidth="10"
                  fill="transparent"
                  strokeDasharray={440}
                  strokeDashoffset={440 - (440 * (analysis?.score || 0)) / 100}
                  className="text-primary transition-all duration-1000 ease-out"
                />
              </svg>
              <div className="absolute inset-0 flex flex-col items-center justify-center">
                <span className="text-4xl font-black text-foreground">{analysis?.score}%</span>
                <span className="text-xs font-bold text-muted-foreground uppercase tracking-widest">Match Global</span>
              </div>
            </div>
            <h3 className="text-xl font-bold mb-2">Excellent Profil !</h3>
            <p className="text-sm text-muted-foreground">
              Votre profil est dans le top 10% des candidats pour les postes de Développeur Frontend Senior.
            </p>
          </div>

          {/* Top Job Matches */}
          <div className="lg:col-span-2 rounded-2xl border bg-card p-8 shadow-sm glass-panel">
            <div className="flex items-center gap-2 mb-6">
              <Target className="text-primary h-5 w-5" />
              <h3 className="text-lg font-bold">Meilleures Opportunités</h3>
            </div>
            <div className="space-y-4">
              {analysis?.top_matches.map((job) => (
                <div key={job.id} className="p-4 rounded-xl border bg-muted/20 hover:bg-muted/40 transition-all flex items-center justify-between group">
                  <div className="flex flex-col">
                    <span className="font-bold text-foreground group-hover:text-primary transition-colors">{job.title}</span>
                    <span className="text-xs text-muted-foreground">{job.company}</span>
                  </div>
                  <div className="flex items-center gap-4">
                    <div className="text-right">
                      <div className="text-sm font-black text-primary">{job.match_score}%</div>
                      <div className="text-[10px] uppercase font-bold text-muted-foreground">Compatibilité</div>
                    </div>
                    <ArrowRight className="h-5 w-5 text-muted-foreground group-hover:text-primary transition-all transform group-hover:translate-x-1" />
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Detailed Breakdown */}
        <div className="grid gap-6 md:grid-cols-2">
          
          {/* Strengths & Weaknesses */}
          <div className="rounded-2xl border bg-card p-8 shadow-sm glass-panel">
            <div className="flex items-center gap-2 mb-8">
              <Trophy className="text-amber-500 h-5 w-5" />
              <h3 className="text-lg font-bold">Analyse des Compétences</h3>
            </div>
            
            <div className="space-y-8">
              <div>
                <h4 className="text-xs font-black uppercase tracking-widest text-emerald-500 mb-4 flex items-center gap-2">
                  <CheckCircle2 size={14} /> Vos Points Forts
                </h4>
                <div className="flex flex-wrap gap-2">
                  {analysis?.strengths.map((s) => (
                    <span key={s} className="px-3 py-1.5 bg-emerald-500/10 text-emerald-500 border border-emerald-500/20 rounded-lg text-sm font-medium">
                      {s}
                    </span>
                  ))}
                </div>
              </div>
              
              <div>
                <h4 className="text-xs font-black uppercase tracking-widest text-destructive mb-4 flex items-center gap-2">
                  <AlertCircle size={14} /> Compétences Manquantes
                </h4>
                <div className="flex flex-wrap gap-2">
                  {analysis?.missing_skills.map((s) => (
                    <span key={s} className="px-3 py-1.5 bg-destructive/10 text-destructive border border-destructive/20 rounded-lg text-sm font-medium">
                      {s}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* AI Career Advisor Recommendations */}
          <div className="rounded-2xl border bg-gradient-to-br from-primary/10 to-blue-500/10 p-8 shadow-sm relative overflow-hidden">
            <div className="relative z-10">
              <div className="flex items-center gap-2 mb-8">
                <Sparkles className="text-primary h-5 w-5" />
                <h3 className="text-lg font-bold">Conseils de l&apos;IA de Carrière</h3>
              </div>
              
              <div className="space-y-6">
                {analysis?.recommendations.map((rec, i) => (
                  <div key={i} className="flex gap-4">
                    <div className="mt-1">
                      <Lightbulb className="text-primary h-5 w-5 opacity-50" />
                    </div>
                    <p className="text-sm text-foreground leading-relaxed">
                      {rec}
                    </p>
                  </div>
                ))}
              </div>

              <button className="mt-10 w-full bg-primary text-primary-foreground py-3 rounded-xl font-bold shadow-lg shadow-primary/20 hover:scale-[1.02] transition-all">
                Optimiser mon CV avec l&apos;IA
              </button>
            </div>
            
            {/* Background Icon */}
            <Sparkles className="absolute -bottom-10 -right-10 h-64 w-64 text-primary opacity-[0.03]" />
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}

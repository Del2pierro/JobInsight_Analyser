"use client";

import { useEffect, useState } from "react";
import DashboardLayout from "@/components/layout/DashboardLayout";
import { TrendsChart } from "@/components/dashboard/TrendsChart";
import { Activity, Briefcase, CheckCircle, TrendingUp, Loader2 } from "lucide-react";
import api from "@/lib/axios";
import { useAuth } from "@/hooks/useAuth";

export default function Home() {
  const { user } = useAuth();
  const [trends, setTrends] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchTrends = async () => {
      try {
        const response = await api.get("/trends/");
        setTrends(response.data);
      } catch (err) {
        console.error("Failed to fetch trends:", err);
        setError("Impossible de charger les données en temps réel.");
      } finally {
        setLoading(false);
      }
    };

    fetchTrends();
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

  return (
    <DashboardLayout>
      <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
        <div>
          <h2 className="text-3xl font-bold tracking-tight">
            Bonjour, {user?.full_name?.split(" ")[0] || "Utilisateur"} 👋
          </h2>
          <p className="text-muted-foreground mt-1">
            {error ? error : "Voici l'analyse en temps réel de votre marché de l'emploi."}
          </p>
        </div>

        {/* Métriques clés - KPI Cards */}
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
          <MetricCard title="Compétences Extraites" value={trends?.top_skills?.length || "0"} icon={<Activity />} trend="Compétences uniques" />
          <MetricCard title="Score de Matching" value="84%" icon={<CheckCircle />} trend="Top 5% des candidats" />
          <MetricCard title="Tendance Marché" value={trends?.market_vibe || "Stable"} icon={<TrendingUp />} trend="Secteur Data & Dev" />
          <MetricCard title="Rapport" value="Prêt" icon={<Briefcase />} trend="PDF disponible" />
        </div>

        {/* Section Principale du Dashboard */}
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-7">
          
          {/* Espace Graphique Principal */}
          <div className="rounded-xl border bg-card text-card-foreground shadow-sm lg:col-span-4 p-6 glass-panel hover-lift">
            <div className="flex flex-col space-y-1.5 mb-2">
              <h3 className="font-semibold leading-none tracking-tight">Évolution de la demande</h3>
              <p className="text-sm text-muted-foreground">Volume d'offres détectées par compétence</p>
            </div>
            
            <TrendsChart data={trends?.top_skills} />
          </div>
          
          {/* Espace Top Compétences */}
          <div className="rounded-xl border bg-card text-card-foreground shadow-sm lg:col-span-3 p-6 glass-panel hover-lift">
            <div className="flex flex-col space-y-1.5 mb-8">
              <h3 className="font-semibold leading-none tracking-tight">Top Compétences Demandées</h3>
              <p className="text-sm text-muted-foreground">Basé sur les dernières offres scrapées</p>
            </div>
            
            <div className="space-y-6">
              {trends?.top_skills?.slice(0, 5).map((skill: any, index: number) => (
                <SkillBar 
                  key={index} 
                  name={skill.name} 
                  percentage={Math.min(Math.round((skill.count / (trends.top_skills[0]?.count || 1)) * 100), 100)} 
                />
              ))}
              {!trends?.top_skills?.length && (
                <p className="text-sm text-muted-foreground italic">Aucune donnée disponible. Lancez un scraping !</p>
              )}
            </div>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}

// Sous-composant pour les cartes d'indicateurs (KPI)
function MetricCard({ title, value, icon, trend }: { title: string, value: string, icon: React.ReactNode, trend: string }) {
  return (
    <div className="rounded-xl border bg-card text-card-foreground shadow-sm p-6 glass-panel hover-lift transition-all duration-300">
      <div className="flex flex-row items-center justify-between space-y-0 pb-2">
        <h3 className="tracking-tight text-sm font-medium text-muted-foreground">{title}</h3>
        <div className="h-8 w-8 text-primary opacity-80">{icon}</div>
      </div>
      <div className="text-3xl font-bold mt-2 text-foreground">{value}</div>
      <p className="text-xs text-muted-foreground mt-3 font-medium bg-primary/10 text-primary w-fit px-2.5 py-1 rounded-full border border-primary/20">
        {trend}
      </p>
    </div>
  );
}

// Sous-composant pour la barre de progression des compétences
function SkillBar({ name, percentage }: { name: string, percentage: number }) {
  return (
    <div className="flex items-center justify-between gap-4 group cursor-default">
      <span className="text-sm font-medium w-28 text-foreground group-hover:text-primary transition-colors">{name}</span>
      <div className="flex-1 h-2.5 bg-muted rounded-full overflow-hidden shadow-inner">
        <div 
          className="h-full bg-primary relative transition-all duration-1000 ease-out" 
          style={{ width: `${percentage}%` }}
        >
          {/* Effet visuel simple avec Tailwind */}
          <div className="absolute top-0 right-0 bottom-0 left-0 bg-white/20 animate-pulse" />
        </div>
      </div>
      <span className="text-sm font-bold w-10 text-right text-primary">{percentage}%</span>
    </div>
  );
}

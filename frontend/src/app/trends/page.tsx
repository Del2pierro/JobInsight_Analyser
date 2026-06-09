"use client";

import DashboardLayout from "@/components/layout/DashboardLayout";
import { TrendsChart } from "@/components/dashboard/TrendsChart";
import { TrendingUp, Map, Briefcase, Globe, Sparkles } from "lucide-react";

export default function TrendsPage() {
  return (
    <DashboardLayout>
      <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
        <div>
          <h2 className="text-3xl font-bold tracking-tight">Tendances du Marché</h2>
          <p className="text-muted-foreground mt-1">
            Analyse macro-économique des données extraites par l'IA sur l'ensemble des offres enregistrées.
          </p>
        </div>

        {/* Top level stats */}
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
          <StatCard title="Demande Globale" value="Très Forte" icon={<TrendingUp />} color="text-green-500" />
          <StatCard title="Ville n°1" value="Paris & IDF" icon={<Map />} color="text-blue-500" />
          <StatCard title="Top Secteur" value="Intelligence Artificielle" icon={<Briefcase />} color="text-purple-500" />
          <StatCard title="Télétravail" value="68% Hybride" icon={<Globe />} color="text-orange-500" />
        </div>

        {/* Charts area */}
        <div className="grid gap-6 lg:grid-cols-2">
          
          {/* Main Area Chart (réutilisé depuis le Dashboard) */}
          <div className="rounded-xl border bg-card text-card-foreground shadow-sm p-6 glass-panel hover-lift flex flex-col">
            <div className="flex flex-col space-y-1.5 mb-2">
              <h3 className="font-semibold leading-none tracking-tight">Croissance Technologique</h3>
              <p className="text-sm text-muted-foreground">Volume de requêtes par technologie sur 6 mois</p>
            </div>
            <div className="flex-1 min-h-[300px]">
              <TrendsChart />
            </div>
          </div>

          {/* New Insights Panel */}
          <div className="rounded-xl border bg-card text-card-foreground shadow-sm p-6 glass-panel flex flex-col hover-lift">
            <div className="flex flex-col space-y-1.5 mb-6">
              <div className="flex items-center gap-2">
                <Sparkles className="h-5 w-5 text-primary" />
                <h3 className="font-semibold leading-none tracking-tight">Insights IA (Synthèse LLM)</h3>
              </div>
              <p className="text-sm text-muted-foreground">Conclusions générées automatiquement</p>
            </div>
            
            <div className="flex-1 space-y-4">
              <InsightItem 
                title="L'explosion de l'IA Générative"
                content="La demande pour des profils maîtrisant les LLMs (Llama, GPT), les bases vectorielles (Qdrant) et l'orchestration (LangChain) a augmenté de 340% ce trimestre."
              />
              <InsightItem 
                title="Le retour au bureau hybride"
                content="Les offres 'Full Remote' stagnent à 15%, tandis que le mode hybride (2 à 3 jours sur site) s'impose comme le nouveau standard de l'industrie."
              />
              <InsightItem 
                title="Python domine, Rust émerge"
                content="Python reste le leader absolu pour la Data et le ML. En parallèle, Rust connaît une croissance fulgurante (+112%) sur les postes Backend nécessitant de la haute performance."
              />
            </div>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}

// Composant Carte Statistique
function StatCard({ title, value, icon, color }: { title: string, value: string, icon: React.ReactNode, color: string }) {
  return (
    <div className="rounded-xl border bg-card shadow-sm p-6 flex items-center gap-5 glass-panel hover-lift transition-all">
      <div className={`p-4 rounded-xl bg-background border ${color} bg-opacity-10 shadow-inner`}>
        {icon}
      </div>
      <div>
        <h3 className="text-sm font-medium text-muted-foreground">{title}</h3>
        <p className="text-2xl font-bold mt-1 text-foreground">{value}</p>
      </div>
    </div>
  );
}

// Composant Insight IA
function InsightItem({ title, content }: { title: string, content: string }) {
  return (
    <div className="p-5 rounded-lg bg-muted/10 border border-muted/30 hover:bg-muted/30 hover:border-primary/30 transition-all duration-300">
      <h4 className="font-semibold text-primary mb-2 text-sm uppercase tracking-wide">{title}</h4>
      <p className="text-sm text-muted-foreground leading-relaxed">{content}</p>
    </div>
  );
}

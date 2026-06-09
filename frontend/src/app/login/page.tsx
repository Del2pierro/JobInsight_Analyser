"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import api from "@/lib/axios";

import { useAuth } from "@/hooks/useAuth";

export default function LoginPage() {
  const { login } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError("");

    try {
      // FastAPI OAuth2PasswordRequestForm expects form-data format, not standard JSON
      const formData = new URLSearchParams();
      formData.append("username", email);
      formData.append("password", password);

      const response = await api.post("/auth/login", formData, {
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
      });

      if (response.data && response.data.access_token) {
        login(response.data.access_token, response.data.refresh_token);
      }
    } catch (err: any) {
      setError(err.response?.data?.message || "Email ou mot de passe incorrect.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex">
      {/* Côté gauche : Branding et Design premium */}
      <div className="hidden lg:flex w-1/2 bg-slate-900 relative flex-col justify-center items-center overflow-hidden border-r border-border/50">
        <div className="absolute inset-0 bg-gradient-to-br from-primary/20 via-background to-background" />
        <div className="relative z-10 text-center px-12 animate-in fade-in slide-in-from-bottom-8 duration-1000">
          <h1 className="text-5xl font-bold mb-6 tracking-tight text-white drop-shadow-lg">JobInsight AI</h1>
          <p className="text-lg text-slate-300 max-w-md mx-auto leading-relaxed">
            Propulsez votre carrière avec l'analyse prédictive et la puissance de l'IA de bout en bout.
          </p>
        </div>
      </div>

      {/* Côté droit : Formulaire de connexion */}
      <div className="flex-1 flex flex-col justify-center px-4 sm:px-6 lg:flex-none lg:w-1/2 bg-background">
        <div className="mx-auto w-full max-w-sm lg:w-[400px] animate-in fade-in duration-700">
          <div>
            <h2 className="mt-6 text-3xl font-bold tracking-tight text-foreground">
              Bon retour parmi nous 👋
            </h2>
            <p className="mt-2 text-sm text-muted-foreground">
              Connectez-vous pour accéder à votre tableau de bord.
            </p>
          </div>

          <div className="mt-8">
            <form onSubmit={handleLogin} className="space-y-6">
              {error && (
                <div className="bg-destructive/10 border border-destructive/20 text-destructive text-sm p-3 rounded-md animate-in slide-in-from-top-2">
                  {error}
                </div>
              )}
              
              <div>
                <label className="block text-sm font-medium text-foreground">Adresse Email</label>
                <div className="mt-2">
                  <input
                    type="email"
                    required
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="block w-full rounded-md border border-input bg-background/50 py-2.5 px-3 text-foreground shadow-sm transition-colors focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary sm:text-sm"
                    placeholder="pierre@exemple.com"
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-foreground">Mot de passe</label>
                <div className="mt-2">
                  <input
                    type="password"
                    required
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="block w-full rounded-md border border-input bg-background/50 py-2.5 px-3 text-foreground shadow-sm transition-colors focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary sm:text-sm"
                    placeholder="••••••••"
                  />
                </div>
              </div>

              <div className="flex items-center justify-between">
                <div className="text-sm">
                  <a href="#" className="font-medium text-primary hover:text-primary/80 transition-colors">
                    Mot de passe oublié ?
                  </a>
                </div>
              </div>

              <button
                type="submit"
                disabled={isLoading}
                className="flex w-full justify-center rounded-md bg-primary py-2.5 px-3 text-sm font-semibold text-primary-foreground shadow-md hover:bg-primary/90 hover:shadow-lg focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary disabled:opacity-50 disabled:cursor-not-allowed transition-all hover-lift"
              >
                {isLoading ? "Connexion en cours..." : "Se connecter"}
              </button>
            </form>

            <div className="mt-6 text-center text-sm text-muted-foreground">
              Pas encore de compte ?{" "}
              <Link href="/register" className="font-medium text-primary hover:text-primary/80 transition-colors">
                Créer un compte
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

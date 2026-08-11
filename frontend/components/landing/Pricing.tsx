"use client";

import { useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Check } from "lucide-react";
import Link from "next/link";
import { useBillingStore } from "@/lib/stores/useBillingStore";

export function Pricing() {
  const { plans, fetchPlans } = useBillingStore();

  useEffect(() => { fetchPlans(); }, [fetchPlans]);

  const sorted = [...plans].sort((a, b) => a.sort_order - b.sort_order);

  return (
    <section id="pricing" className="py-20 bg-gray-50">
      <div className="max-w-[1200px] mx-auto px-6">
        <div className="text-center mb-14">
          <h2 className="text-3xl font-bold text-gray-900 tracking-tight">
            Harga yang transparan
          </h2>
          <p className="mt-3 text-gray-500 text-lg">
            Mulai gratis, upgrade sesuai kebutuhan.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-4xl mx-auto">
          {sorted.map((plan) => (
            <div
              key={plan.id}
              className={`relative bg-white rounded-xl p-7 border transition-shadow ${
                plan.is_popular
                  ? "border-blue-600 shadow-lg ring-1 ring-blue-600"
                  : "border-gray-200 shadow-sm hover:shadow-md"
              }`}
            >
              {plan.is_popular && (
                <div className="absolute -top-3 left-1/2 -translate-x-1/2 bg-blue-600 text-white text-xs font-medium px-3 py-0.5 rounded-full">
                  POPULAR
                </div>
              )}
              <h3 className="text-lg font-semibold text-gray-900">{plan.name}</h3>
              <p className="text-sm text-gray-500 mt-1">{plan.description}</p>
              <div className="mt-5 mb-6">
                <span className="text-3xl font-bold text-gray-900">{plan.price_monthly}</span>
                <span className="text-sm text-gray-500">/bulan</span>
              </div>
              <ul className="space-y-3 mb-8">
                {(plan.features || []).map((f) => (
                  <li key={f} className="flex items-center gap-2 text-sm text-gray-600">
                    <Check className="w-4 h-4 text-blue-600 shrink-0" />
                    {f}
                  </li>
                ))}
              </ul>
              <Link href="/register">
                <Button
                  className={`w-full font-medium text-sm h-10 ${
                    plan.is_popular
                      ? "bg-blue-600 hover:bg-blue-700 text-white"
                      : "bg-white border border-gray-300 text-gray-700 hover:bg-gray-50"
                  }`}
                  variant={plan.is_popular ? "default" : "outline"}
                >
                  {plan.cta_text || "Pilih Plan"}
                </Button>
              </Link>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

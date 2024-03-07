monomer_6dj4 = textread("Cry1Ab/Structural_Info/monomer_6dj4_allatom_8");
intradomain_N_DI = textread("Cry1Ab/Domains/Endotoxin_N/Endotoxin_N_align_ranked_matched.DI");
intradomain_M_DI = textread("Cry1Ab/Domains/Endotoxin_M/Endotoxin_M_align_ranked_matched.DI");
intradomain_C_DI = textread("Cry1Ab/Domains/Endotoxin_C/Endotoxin_C_align_ranked_matched.DI");
%interdomain_NM_DI = textread("PFam_Domains/BTR1_concat_3_NM_ranked_mapped.DI");
%interdomain_NC_DI = textread("PFam_Domains/BTR1_concat_3_NC_ranked_mapped.DI");
%interdomain_MC_DI = textread("PFam_Domains/BTR1_concat_3_MC_ranked_mapped.DI");
%%
plotDCAmap(monomer_6dj4, [], [1,600], 0, 1);
plotDCAmap(intradomain_N_DI(1:350, :), [], [1,600], 0, 0);
plotDCAmap(intradomain_M_DI(1:350, :), [], [1,600], 0, 0);
plotDCAmap(intradomain_C_DI(1:350, :), [], [1,600], 0, 0);
%%
plotDCAmap(interdomain_NM_DI(1:100, :), [], [1,600], 0, 0);
plotDCAmap(interdomain_MC_DI(1:100, :), [], [1,600], 0, 0);
plotDCAmap(interdomain_NC_DI(1:100, :), [], [1,600], 0, 0);
%%
yline(223);
%%
xline(433);
yline(433);
monomer_6dj4 = textread("~/Projects/BT_R1/Cry1Ab/Structural_Info/monomer_6dj4_allatom_8");
intradomain_M_DI = textread("M_align_ranked_matched.DI");
intradomain_C_DI = textread("C_align_ranked_matched.DI");
interdomain_MC_DI = textread("MC_concat_ranked_mapped.DI");
%%
plotDCAmap(monomer_6dj4, [], [1,600], 0, 1);
plotDCAmap(intradomain_M_DI(1:300, :), [], [1,600], 0, 0);
plotDCAmap(intradomain_C_DI(1:200, :), [], [1,600], 0, 0);
%%
plotDCAmap(interdomain_MC_DI(1:100, :), [], [1,600], 0, 0);
%%
yline(223);
%%
xline(433);
yline(433);
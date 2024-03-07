monomer_6dj4 = textread("~/Projects/BT_R1/Cry1Ab/Structural_Info/monomer_6dj4_allatom_8");
DI_pairs = textread("3D_MSA_ranked.DI");
%%
plotDCAmap(monomer_6dj4, [], [1,600], 0, 1);
plotDCAmap(DI_pairs(1:2500, :), [], [1,600], 0, 0);
%%
yline(223);
%%
xline(433);
yline(433);
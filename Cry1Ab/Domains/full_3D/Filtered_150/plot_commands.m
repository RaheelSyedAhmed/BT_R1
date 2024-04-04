native_contacts = textread('~/Projects/BT_R1/Cry1Ab/Structural_Info/monomer_6dj4_allatom_8');
DI_pairs = textread('~/Projects/BT_R1/Cry1Ab/Domains/full_3D/Filtered_150/Berliner_3D_align_ranked_matched.DI');
%%
plotDCAmap(native_contacts, [], [1, 100], 0, 1);
plotDCAmap(DI_pairs(1:1500, :), [], [1,110], 0, 0);
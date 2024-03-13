native_contacts = textread('~/Projects/BT_R1/EC12/Structural_Info/monomer_7tni_allatom_8');
DI_pairs = textread('~/Projects/BT_R1/EC12/Coevolutionary_Info/Filtered_41/EC12_align_ranked_matched.DI');
%%
plotDCAmap(native_contacts, [], [1, 100], 0, 1);
plotDCAmap(DI_pairs(1:300, :), [], [1,110], 0, 0);
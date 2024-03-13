native_contacts = textread('Structural_Info/monomer_7tni_allatom_8');
DI_pairs = textread('Coevolutionary_Info/EC12_align_ranked_matched.DI');
%%
plotDCAmap(native_contacts, [], [1, 100], 0, 1);
plotDCAmap(DI_pairs(1:600, :), [], [1,110], 0, 0);
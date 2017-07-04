## history format
```
PATCH_ITEM ::= * VERSIONS  PATCH_TITLE {CHARACTERISTIC::ASPECT} \n PATCH_CHANGS
VERSIONS ::= '['BEGIN_VERSION - END_VERSION']'|'['BEGIN_VERSION']'
BEGIN_VERSION|END_VERSION ::= [2..4].[0..18].[22..29]
PATCH_TITLE ::= TITLE.patch 
TITLE|DESCRIPT = ['a'..'z','A'..'Z']*|NULL //string or nothing
CHARACTERISTIC ::='C'
ASPECT ::= FEATURE|FIXBUG|PERFORMANCE|MAINTAIN
FEATURE ::= 'feature'::TITLE[::DESCRIPT]
FIXBUG ::= 'fixbug'::BUG_CONCREQUENCE::BUG_TYPE::FIX_METHOD::DESCRIPT
BUG_CONCREQUENCE ::='corrupt'|'hang'|'crash'|'leak'|'??'|...
BUG_TYPE ::= SEMANTIC|CONCURRENCY|MEMORY|ERRORCODE
SEMANTIC ::= 'hardware'|'softirq'|'migration'|'preempt'|'irq'|...
CONCURRENCY ::= 'atomicity'|'order'|'deadlock'|'livelock'|...
MEMORY ::= 'resource leak'|'uninit var'|'buf overflow'|...
ERRORCODE ::= 'compiling err'|'config err'|...
FIX_METHOD ::= 'hardware'|'lock'|'irq'|'preempt'|'migration'|...
PERFORMANCE ::= 'performance'::PERF_METHOD::DESCRIPT
PERF_METHOD ::= 'cache'|'msleep'|...
MAINTAIN ::='maintain'::MAINTAIN_METHOD
```

### PATCH_CHANGES
```
      + [[file:2.6.22/new-softirq-code.patch][2.6.22]]  {MOD::KER_MOD}
      M [[file:2.6.23/new-softirq-code.patch][2.6.23]]
        [[file:2.6.24/new-softirq-code.patch][2.6.24]]
      M [[file:2.6.25/new-softirq-code.patch][2.6.25]]
        [[file:2.6.26/new-softirq-code.patch][2.6.26]]
      - 2.6.29

   Meaning of the first character:

      [+]        This patch is introduced in this version (not seen in previous ones).
      [-]        This patch appears in the previous version but disappears in this one.
      [ ]        This patch is seen in both the previous and current version.
                 This patch is identical in the two versions.
      [m]        This patch is seen in both the previous and current version.
                 The changed lines in the patches are identical, but the contexts are not.
      [M]        This patch is seen in both the previous and current version.
                 The changed lines in the patches are different.

      KER_MOD    The 1~2 level directories(means kernel modules) of kernel src code, such as  kernel, 
                 mm, fs, net, drivers/acpi, drivers, lib, include/linux ... 
```

### example
```
* [2.6.22         ] slob-scale-break-out-caches.patch {C::performance::cache::use kmem_cache,remove global slobfree}
  + [[file:2.6.22/slob-scale-break-out-caches.patch][2.6.22]]  {MOD::mm}

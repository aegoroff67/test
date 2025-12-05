# AssessmentPage.js Refactoring Plan

## Current State Analysis

**File Size**: 1,281 lines (critically bloated)

### Problems Identified:

1. **State Management Bloat** (Lines 78-95)
   - 18 state variables for modal management
   - 9 `show*Modal` states
   - 9 `is*Selected` states

2. **Handler Function Repetition** (Lines 374-443)
   - 18 nearly identical handler functions
   - 9 `handleOpen*Modal` functions
   - 9 `handleClose*Modal` functions

3. **Modal Rendering Duplication** (Lines 1167-1276)
   - 9 identical modal render blocks
   - Each block is ~15 lines
   - Only differences: component name, data source, handlers

4. **Import Bloat** (Lines 28-45)
   - 9 modal component imports
   - 9 JSON data imports

5. **Technical Debt**
   - Code is difficult to maintain
   - Adding a 10th framework would require ~50 more lines
   - High risk of copy-paste errors
   - Testing complexity increases linearly

---

## Recommended Refactoring Approaches

### 🏆 **Option 1: Generic Modal with Configuration (RECOMMENDED)**

**Impact**: Reduce from 1,281 to ~900 lines (~30% reduction)

#### Implementation:

```javascript
// 1. Create a single configuration object
const FRAMEWORK_CONFIG = {
  faira: {
    id: 'faira',
    name: 'FAIRA',
    component: FairaAlignmentModal,
    data: fairaAlignmentData,
    color: 'amber'
  },
  nist: {
    id: 'nist',
    name: 'NIST AI RMF',
    component: NistAlignmentModal,
    data: nistAlignmentData,
    color: 'indigo'
  },
  // ... 7 more frameworks
};

// 2. Replace 18 state variables with 1 state object
const [activeModal, setActiveModal] = useState(null);

// 3. Replace 18 handler functions with 2 generic handlers
const handleOpenModal = (frameworkId) => {
  setActiveModal(frameworkId);
};

const handleCloseModal = () => {
  setActiveModal(null);
};

// 4. Replace 9 modal render blocks with 1 dynamic renderer
{Object.entries(FRAMEWORK_CONFIG).map(([key, config]) => {
  const ModalComponent = config.component;
  const alignmentData = config.data[currentQuestion?.code];
  
  if (!currentQuestion || !alignmentData) return null;
  
  return (
    <ModalComponent
      key={key}
      isOpen={activeModal === key}
      onClose={handleCloseModal}
      questionCode={currentQuestion.code}
      questionText={currentQuestion.text}
      alignmentData={alignmentData}
    />
  );
})}
```

#### Pros:
- ✅ Massive code reduction (~380 lines removed)
- ✅ Single source of truth for framework configuration
- ✅ Easy to add new frameworks (just add to config object)
- ✅ Reduced risk of copy-paste errors
- ✅ Easier testing and maintenance
- ✅ Can be implemented incrementally

#### Cons:
- ⚠️ Requires careful testing of all 9 modals
- ⚠️ Moderate refactoring effort (~2-3 hours)

---

### 💎 **Option 2: Unified Modal Component (ULTIMATE SOLUTION)**

**Impact**: Reduce from 1,281 to ~600 lines (~50% reduction)

#### Implementation:

```javascript
// 1. Create a single, highly configurable modal component
// File: /app/frontend/src/components/UnifiedAlignmentModal.js

export default function UnifiedAlignmentModal({ 
  isOpen, 
  onClose, 
  questionCode, 
  questionText,
  framework,
  alignmentData 
}) {
  const config = FRAMEWORK_DISPLAY_CONFIG[framework];
  
  return (
    <div className="fixed inset-0 z-50 ...">
      <div className="bg-white rounded-lg ...">
        {/* Dynamic Header */}
        <div className={`bg-${config.color}-600 text-white p-6`}>
          <h2>{config.title}</h2>
          <p>{questionCode}: {questionText}</p>
        </div>
        
        {/* Dynamic Content Renderer */}
        <div className="p-6">
          {config.sections.map(section => (
            <DynamicSection 
              key={section.id}
              section={section}
              data={alignmentData}
            />
          ))}
        </div>
      </div>
    </div>
  );
}

// 2. Configuration for all frameworks
const FRAMEWORK_DISPLAY_CONFIG = {
  faira: {
    title: 'FAIRA Alignment Information',
    color: 'amber',
    sections: [
      { id: 'overview', label: 'Overview', field: 'overview', style: 'amber' },
      { id: 'partB', label: 'Part B', field: 'fairaComponent.partB', style: 'gray' },
      // ...
    ]
  },
  // ... other frameworks
};

// 3. In AssessmentPage.js
const [activeFramework, setActiveFramework] = useState(null);

<UnifiedAlignmentModal
  isOpen={!!activeFramework}
  onClose={() => setActiveFramework(null)}
  framework={activeFramework}
  questionCode={currentQuestion?.code}
  questionText={currentQuestion?.text}
  alignmentData={
    activeFramework && FRAMEWORK_CONFIG[activeFramework]?.data[currentQuestion?.code]
  }
/>
```

#### Pros:
- ✅ Maximum code reduction (~680 lines removed)
- ✅ Single modal component for all frameworks
- ✅ Highly maintainable
- ✅ Can delete 9 individual modal files
- ✅ Consistent UI behavior across all frameworks
- ✅ Much easier to add framework #10

#### Cons:
- ⚠️ Major refactoring effort (~1 day)
- ⚠️ Requires extensive testing of all 9 frameworks
- ⚠️ More complex initial implementation
- ⚠️ Need to carefully map all framework-specific fields

---

### 🔧 **Option 3: Custom Hook Pattern (INTERMEDIATE)**

**Impact**: Reduce from 1,281 to ~1,000 lines (~22% reduction)

#### Implementation:

```javascript
// File: /app/frontend/src/hooks/useFrameworkModals.js
export function useFrameworkModals(frameworks) {
  const [modals, setModals] = useState({});
  
  const openModal = (frameworkId) => {
    setModals(prev => ({ ...prev, [frameworkId]: true }));
  };
  
  const closeModal = (frameworkId) => {
    setModals(prev => ({ ...prev, [frameworkId]: false }));
  };
  
  const isModalOpen = (frameworkId) => modals[frameworkId] || false;
  
  return { openModal, closeModal, isModalOpen };
}

// In AssessmentPage.js
const { openModal, closeModal, isModalOpen } = useFrameworkModals();

// Replace all individual handlers with:
onClick={() => openModal('faira')}
onClose={() => closeModal('faira')}
isOpen={isModalOpen('faira')}
```

#### Pros:
- ✅ Moderate code reduction
- ✅ Reusable hook pattern
- ✅ Easier to test modal logic
- ✅ Least risky approach

#### Cons:
- ⚠️ Still have 9 separate modal components
- ⚠️ Still have repetitive render blocks
- ⚠️ Limited long-term scalability

---

## Comparison Matrix

| Approach | Lines Reduced | Effort | Risk | Maintainability | Scalability |
|----------|---------------|--------|------|-----------------|-------------|
| **Option 1** (Config) | ~380 | Medium | Low | High | Excellent |
| **Option 2** (Unified) | ~680 | High | Medium | Very High | Excellent |
| **Option 3** (Hook) | ~280 | Low | Very Low | Medium | Good |

---

## Migration Path Recommendations

### 🎯 **Immediate Action (Current Sprint)**
Implement **Option 1** (Generic Modal with Configuration)
- Best balance of impact vs. effort
- Can be done in 2-3 hours
- Low risk with proper testing
- Immediate 30% code reduction

### 🚀 **Future Enhancement (Next Sprint)**
Consider **Option 2** (Unified Modal Component)
- Only if more frameworks will be added
- Best for long-term maintainability
- Requires dedicated time for thorough testing

### 📊 **Bonus: Add These Improvements Regardless**

1. **Extract Framework Configuration to Separate File**
   ```javascript
   // /app/frontend/src/config/frameworksConfig.js
   export const FRAMEWORKS = { ... };
   ```

2. **Create Framework Badge Component**
   ```javascript
   // /app/frontend/src/components/FrameworkBadge.js
   export default function FrameworkBadge({ framework, onClick, isAvailable }) {
     // Reusable badge logic
   }
   ```

3. **Add PropTypes or TypeScript**
   - Prevent prop-passing errors
   - Better IDE support

4. **Create Unit Tests**
   ```javascript
   // Test modal open/close logic
   // Test framework configuration loading
   ```

---

## Implementation Checklist for Option 1

- [ ] Create `FRAMEWORK_CONFIG` object with all 9 frameworks
- [ ] Replace 18 state variables with single `activeModal` state
- [ ] Replace 18 handlers with `handleOpenModal(id)` and `handleCloseModal()`
- [ ] Update all badge `onClick` handlers to use new generic handler
- [ ] Replace 9 modal render blocks with single `.map()` renderer
- [ ] Test each modal individually
- [ ] Test modal switching (open multiple in sequence)
- [ ] Verify all data displays correctly
- [ ] Check mobile responsiveness
- [ ] Update documentation

---

## Risk Mitigation

1. **Create Feature Branch**
   - Don't refactor directly on main
   - Allows easy rollback if issues found

2. **Test Thoroughly**
   - Manual testing of all 9 modals
   - Test with real assessment data
   - Verify modal close behavior
   - Check keyboard navigation (Escape key)

3. **Incremental Rollout**
   - Start with 2-3 frameworks
   - Verify behavior matches original
   - Gradually add remaining frameworks

4. **Keep Original Code**
   - Comment out rather than delete initially
   - Allows quick comparison if bugs found

---

## Estimated Timeline

### Option 1 (Recommended):
- **Planning**: 30 minutes
- **Implementation**: 2 hours
- **Testing**: 1 hour
- **Documentation**: 30 minutes
- **Total**: ~4 hours

### Option 2 (Future):
- **Planning**: 1 hour
- **Implementation**: 5 hours
- **Testing**: 2 hours
- **Documentation**: 1 hour
- **Total**: ~1 day

### Option 3 (Quick Fix):
- **Planning**: 15 minutes
- **Implementation**: 1 hour
- **Testing**: 30 minutes
- **Total**: ~2 hours

---

## Additional Benefits

After refactoring, you'll gain:

1. **Faster Feature Additions**
   - Adding framework #10 will take 5 minutes instead of 30

2. **Easier Debugging**
   - Single configuration point
   - Consistent behavior across all modals

3. **Better Code Reviews**
   - Reviewers can focus on logic, not repetition
   - Easier to spot bugs

4. **Reduced Merge Conflicts**
   - Fewer lines = fewer conflicts
   - Configuration changes isolated

5. **Performance**
   - React can optimize single modal switching
   - Smaller bundle size (if using unified component)

---

## Conclusion

**Immediate Recommendation**: Start with **Option 1**

This provides the best return on investment and sets the foundation for future improvements. The code will be much more maintainable, and adding new frameworks will become trivial.

If you decide to proceed, I can implement Option 1 immediately and have it tested within a few hours.

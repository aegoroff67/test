// Helper functions for Awareness Assessment support

export const getResponseOptions = (assessmentType, predefinedAnswers) => {
  if (assessmentType === 'Awareness') {
    return [
      {
        value: 'EARLY_AWARENESS',
        label: 'Early Awareness',
        score: 1,
        text: predefinedAnswers?.early_awareness || 'Limited or no understanding'
      },
      {
        value: 'EXPLORING_OPPORTUNITIES',
        label: 'Exploring Opportunities',
        score: 2,
        text: predefinedAnswers?.exploring_opportunities || 'Beginning to explore possibilities'
      },
      {
        value: 'BUILDING_READINESS',
        label: 'Building Readiness',
        score: 3,
        text: predefinedAnswers?.building_readiness || 'Actively preparing and building capabilities'
      },
      {
        value: 'READY_TO_PROGRESS',
        label: 'Ready to Progress',
        score: 4,
        text: predefinedAnswers?.ready_to_progress || 'Ready to implement and advance'
      }
    ];
  }
  
  if (assessmentType === 'Readiness') {
    return [
      {
        value: 'FOUNDATIONAL',
        label: 'Foundational',
        score: 1,
        text: predefinedAnswers?.foundational || 'Minimal or no capability in place'
      },
      {
        value: 'DEVELOPING',
        label: 'Developing',
        score: 2,
        text: predefinedAnswers?.developing || 'Emerging capability with gaps'
      },
      {
        value: 'ESTABLISHED',
        label: 'Established',
        score: 3,
        text: predefinedAnswers?.established || 'Strong capability with consistent practice'
      },
      {
        value: 'LEADING',
        label: 'Leading',
        score: 4,
        text: predefinedAnswers?.leading || 'Mature capability with continuous improvement'
      }
    ];
  }
  
  if (assessmentType === 'Orgwide') {
    return [
      {
        value: 'FOUNDATIONAL',
        label: 'Foundational',
        score: 1,
        text: predefinedAnswers?.foundational || 'Minimal or no capability in place'
      },
      {
        value: 'DEVELOPING',
        label: 'Developing',
        score: 2,
        text: predefinedAnswers?.developing || 'Emerging capability with gaps'
      },
      {
        value: 'ESTABLISHED',
        label: 'Established',
        score: 3,
        text: predefinedAnswers?.established || 'Strong capability with consistent practice'
      },
      {
        value: 'LEADING',
        label: 'Leading',
        score: 4,
        text: predefinedAnswers?.leading || 'Mature capability with continuous improvement'
      }
    ];
  }
  
  // Default System assessment options (ordered: Foundational → Leading)
  return [
    {
      value: 'FOUNDATIONAL',
      label: 'Foundational',
      score: 1,
      text: predefinedAnswers?.foundational || 'Little to no implementation or consideration'
    },
    {
      value: 'DEVELOPING',
      label: 'Developing',
      score: 2,
      text: predefinedAnswers?.developing || 'Minimal implementation, significant gaps exist'
    },
    {
      value: 'ESTABLISHED',
      label: 'Established',
      score: 3,
      text: predefinedAnswers?.established || 'Solid implementation with room for improvement'
    },
    {
      value: 'LEADING',
      label: 'Leading',
      score: 4,
      text: predefinedAnswers?.leading || 'Comprehensive implementation with best practices and full compliance'
    },
    {
      value: 'OTHER',
      label: 'Other',
      score: 0,
      text: 'Provide your own response'
    }
  ];
};

export const getColorScheme = (assessmentType) => {
  if (assessmentType === 'Awareness') {
    return {
      primary: 'green-600',
      primaryHover: 'green-700',
      light: 'green-50',
      border: 'green-100',
      text: 'green-600',
      badge: 'green-100',
      badgeText: 'green-800'
    };
  }
  
  if (assessmentType === 'Readiness') {
    return {
      primary: 'blue-600',
      primaryHover: 'blue-700',
      light: 'blue-50',
      border: 'blue-100',
      text: 'blue-600',
      badge: 'blue-100',
      badgeText: 'blue-800'
    };
  }
  
  if (assessmentType === 'Orgwide') {
    return {
      primary: 'purple-600',
      primaryHover: 'purple-700',
      light: 'purple-50',
      border: 'purple-100',
      text: 'purple-600',
      badge: 'purple-100',
      badgeText: 'purple-800'
    };
  }
  
  // Default teal for System
  return {
    primary: 'teal-600',
    primaryHover: 'teal-700',
    light: 'teal-50',
    border: 'teal-100',
    text: 'teal-600',
    badge: 'teal-100',
    badgeText: 'teal-800'
  };
};
